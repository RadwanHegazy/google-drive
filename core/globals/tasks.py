from datetime import datetime, timedelta
from django.core.cache import cache
from file.models import UserFile
from .celery_app import app
from users.models import User
from .chunking.utlities import clear_chunks

@app.task
def chunk_collector(user_id) :
    """Collect all chunks for a user and process them."""

    user = User.objects.filter(id=user_id)
    if not user.exists():
        return "User does not exist."
    
    user = user.first()

    head = cache.get(f"chunk_head_{user_id}", None)
    filename = head.get("filename")
    content_type = head.get("content_type")

    if not head:
        return "No chunks to process."

    head = f'chunk_head_{user_id}'
    chunks = []
    total_size_in_kb = 0
    while head:
        chunk_data = cache.get(head)
        if chunk_data:
            chunks.append(chunk_data.get('chunk', b''))
            ch_size = chunk_data.get('chunk_size_in_kb', 0)
            total_size_in_kb += ch_size
        next_chunk_key = chunk_data.get('next', None)
        head = next_chunk_key

    filepath = f"media/uploads/{filename}"
    with open(filepath, 'wb') as f:
        f.writelines(chunks)
        f.close()

    user_file = UserFile.objects.create(
        name=filename,
        content_type=content_type,
        owner=user,
        file_size_in_giga=total_size_in_kb / (1024 * 1024),  # Convert KB to GB
        file=filepath,
    )

    user_file.save()

    clear_chunks(user_id)
    return f"Processed {len(chunks)} chunks successfully."

@app.task
def clear_expired_sessions():
    """Clear expired chunks from the cache."""
    keys = cache.keys('chunk_head_*')
    current = datetime.now()
    for key in keys:
        chunk_data = cache.get(key)
        if chunk_data['created_at'] < current - timedelta(days=1):
            try : 
                clear_chunks(key.split('_')[-1]) 
            except Exception as e:
                print(f"Error clearing chunks for {key}: {e}")