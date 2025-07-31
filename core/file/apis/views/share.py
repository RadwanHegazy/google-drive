from users.models import User
from file.models import UserFile
from rest_framework.exceptions import ValidationError
from file.apis.serializers import ShareFileSerializer, RemoveFromSharedSerializer
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from file.permissions import CanViewFile

class ShareFilesAPI (CreateAPIView) : 
    serializer_class = ShareFileSerializer
    permission_classes = [IsAuthenticated]


class RemoveSharedUsersAPI (DestroyAPIView) :
    permission_classes = [CanViewFile]
    serializer_class = RemoveFromSharedSerializer
    lookup_field = 'id'
    queryset = UserFile.objects.all()

    def perform_destroy(self, instance : UserFile):
        data = self.request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        users = serializer.data.get('users')
        instance.shared_with.remove(*users)
        instance.save()