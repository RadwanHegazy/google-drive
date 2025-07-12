from globals.views import DeleteCachedAPI
from rest_framework.permissions import IsAdminUser
from plan.models import StoragePlan

class DeleteStoragePlanAPI (DeleteCachedAPI) :
    permission_classes = [IsAdminUser]
    lookup_field = 'id'
    cache_key = 'plans'
    cache_model = StoragePlan