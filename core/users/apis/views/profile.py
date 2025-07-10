from rest_framework.generics import RetrieveAPIView
from users.apis.serializers.profile import ProfileSerializer
from rest_framework.permissions import IsAuthenticated

class UserProfileAPI (RetrieveAPIView) : 
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    