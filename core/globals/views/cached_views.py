from django.core.cache import cache
from datetime import timedelta
from django.db.models import Model, QuerySet
from typing import Optional
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

class CacheView:
    """
    A base class for caching Django model querysets.

    This class provides functionality to cache Django model querysets and retrieve them
    efficiently. It helps reduce database load by storing querysets in Django's cache
    backend.

    Attributes:
        cache_model (Optional[Model]): The Django model class to cache querysets for.
            Must be set in subclasses.
        cache_key (Optional[str]): The key used to store/retrieve data from cache.
            Can be set directly or via get_cache_key().
        cache_timeout (timedelta): How long to keep items in cache before expiring.
            Defaults to 2 hours.
    """
    cache_model: Optional[Model] = None
    cache_key: Optional[str] = None
    cache_timeout = timedelta(hours=2)

    def get_cache_key(self) -> Optional[str]:
        """Override this method to provide a custom cache key"""
        return None

    def validate_settings(self, cache_key: str) -> None:
        """Validate cache settings before querying"""
        if not cache_key:
            raise ValueError("Cache key must be set via `cache_key` or `get_cache_key()`")
        
        if self.cache_model == None and self.get_cache_value() == None:
            raise ValueError("attr `cache_model` or method `get_cache_value()` must set one of them")
            

    def get_queryset(self) -> QuerySet:
        """Get queryset from cache or database"""
        cache_key = self.cache_key or self.get_cache_key()
        self.validate_settings(cache_key)
        
        # Try to get data from cache first
        queryset = cache.get(cache_key)
        
        if not queryset:
            # Cache miss - get from database and cache it
            queryset = self.cache_model.objects.all() if self.cache_model else self.get_cache_value()
            cache.set(
                cache_key,
                queryset,
                timeout=int(self.cache_timeout.total_seconds())
            )
        return queryset

    def get_cache_value(self) : 
        return None
    

class ListCachedAPI (
    CacheView,
    ListAPIView
) : ...

class RetrieveCachedAPI (
    CacheView,
    RetrieveAPIView
) : ...

class UpdateCachedAPI (
    CacheView,
    UpdateAPIView
) : ...

class DeleteCachedAPI (
    CacheView,
    DestroyAPIView
) : ...

