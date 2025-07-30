from django.core.cache import cache
from datetime import datetime, timedelta
from uuid import uuid4
from globals.tasks import chunk_collector
from core.settings import TESTING

class SessionHandler : 
    """Handle the session for chunking operations."""

    def __init__(self, user_id):
        self.user_id = user_id
    
    def start_session(self, filename, content_type):
        """Start a new session for chunking."""
        head = f"chunk_head_{self.user_id}"
        cache.set(
            head, 
            self._set_body(
                filename = filename,
                content_type = content_type
            ),
            timeout=timedelta(days=1).total_seconds()  
        )

    def add_chunk(self, chunk, chunk_size_in_kb):
        """Add a chunk as a node in a linked list stored in cache."""
        chunk_val = self._set_body(
            chunk=chunk,
            chunk_size_in_kb=chunk_size_in_kb
        )
        chunk_key = str(uuid4())
        cache.set(chunk_key, chunk_val, timeout=timedelta(days=1).total_seconds())

        head_key = f"chunk_head_{self.user_id}"
        head = cache.get(head_key)
        
        current_key = head.get('next')
        prev_key = head_key
        while current_key:
            current_node = cache.get(current_key)
            if not current_node or not current_node.get('next'):
                break
            prev_key = current_key
            current_key = current_node.get('next')
        # Link the last node to the new chunk
        if current_key:
            current_node = cache.get(current_key)
            current_node['next'] = chunk_key
            cache.set(current_key, current_node, timeout=timedelta(days=1).total_seconds())
        else:
            # Only head exists, link head to first chunk
            head['next'] = chunk_key
            cache.set(head_key, head, timeout=timedelta(days=1).total_seconds())

    def _set_body(self,  **kwargs) :
        return {
            **kwargs,
            'created_at' : datetime.now(),
            'next': None,
        }

    def process_chunks(self):
        """Process all chunks for the user."""
        if TESTING:
            chunk_collector(self.user_id)
        else:
            chunk_collector.delay(self.user_id)