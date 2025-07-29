from django.core.cache import cache
from datetime import datetime, timedelta
from uuid import uuid4
from globals.tasks import chunk_collector

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
        """Set the next chunk to be processed."""
        chunk_val = self._set_body(
            chunk=chunk,
            chunk_size_in_kb=chunk_size_in_kb
        )
        chunk_key = str(uuid4())
        cache.set(chunk_key, chunk_val, timeout=timedelta(days=1).total_seconds())

        head = cache.get(f"chunk_head_{self.user_id}", None)
        while head: 
            next = head.get('next', None)
            if not next:
                head['next'] = chunk_key
                break
            head = next

    def _set_body(self,  **kwargs) :
        return {
            **kwargs,
            'created_at' : datetime.now(),
            'next': None,
        }

    def process_chunks(self):
        """Process all chunks for the user."""
        chunk_collector.delay(self.user_id)
    