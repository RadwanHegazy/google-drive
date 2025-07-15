from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from plan.apis.serializers import CancelChecoutSerializer

class CancelSubscribeAPI (CreateAPIView) :
    """Implement cancel subscribtion for authenticated users"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CancelChecoutSerializer
