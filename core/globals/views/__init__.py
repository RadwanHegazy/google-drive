from rest_framework.generics import CreateAPIView
from .cached_views import (
    ListCachedAPI,
    RetrieveCachedAPI,
    DeleteCachedAPI,
    UpdateCachedAPI,
)