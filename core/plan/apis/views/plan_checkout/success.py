from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from plan.apis.serializers import SuccessChecoutSerializer

class SuccessSubscribeAPI (CreateAPIView) :
    """Implement success Subscribtion for authenticated users"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SuccessChecoutSerializer
