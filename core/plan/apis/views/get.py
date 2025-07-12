from globals.views import ListCachedAPI, RetrieveCachedAPI
from plan.apis.serializers import StoragePlanSerializer
from plan.models import StoragePlan

class ListStoragePlanAPI (ListCachedAPI) :
    serializer_class = StoragePlanSerializer
    cache_key = 'plans'
    cache_model = StoragePlan

class RetrieveStoragePlanAPI (RetrieveCachedAPI) :
    serializer_class = StoragePlanSerializer
    lookup_field = 'id'
    cache_key = 'plans'
    cache_model = StoragePlan
