from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import StoragePlan
from django.core.cache import cache

@receiver([post_save, post_delete], sender=StoragePlan)
def delete_cached_data(**kwargs) : 
    cache.delete('plans')