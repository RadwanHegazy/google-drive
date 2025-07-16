from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from file.models import UserFile


class DeleteUserFielAPI (DestroyAPIView) : 
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return UserFile.objects.filter(
            owner = self.request.user,
            is_deleted = False
        )