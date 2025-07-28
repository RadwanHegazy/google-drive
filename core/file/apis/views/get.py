from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from file.models import UserFile
from file.apis.serializers import ListUserFileSerializer, RetrieveUserFileSerializer
from file.permissions import CanViewFile

class ListUserFielAPI (ListAPIView) : 
    permission_classes = [IsAuthenticated]
    serializer_class = ListUserFileSerializer
    
    def get_queryset(self):
        return UserFile.objects.filter(
            owner = self.request.user,
            is_deleted = False
        )

class RetrieveUserFielAPI (RetrieveAPIView) : 
    permission_classes = [CanViewFile]
    serializer_class = RetrieveUserFileSerializer
    queryset = UserFile.objects.filter(is_deleted=False)
    lookup_field = 'id'