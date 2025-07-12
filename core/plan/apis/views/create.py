from globals.views import CreateAPIView
from plan.apis.serializers import StoragePlanSerializer
from rest_framework.permissions import IsAdminUser

class CreateStoragePlanAPI (CreateAPIView) :
    serializer_class = StoragePlanSerializer
    permission_classes = [IsAdminUser]