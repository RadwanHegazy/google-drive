from django.core.cache import cache

def clear_chunks (user_id) : 
    next = f"chunk_head_{user_id}"
    while next:
        next_chanks = cache.get(next, None)
        cache.delete(next)
        next = next_chanks.get('next', None)