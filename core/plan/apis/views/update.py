from globals.views import UpdateCachedAPI
from rest_framework.permissions import IsAdminUser
from plan.apis.serializers import StoragePlanSerializer
from plan.models import StoragePlan

class UpdateStoragePlanAPI (UpdateCachedAPI) :
    permission_classes = [IsAdminUser]
    serializer_class = StoragePlanSerializer
    lookup_field = 'id'
    cache_key = 'plans'
    cache_model = StoragePlan