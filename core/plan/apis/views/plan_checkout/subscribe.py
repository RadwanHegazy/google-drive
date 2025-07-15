from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from plan.apis.serializers import CheckoutSerializer

class UserPlanSubscribeAPI (CreateAPIView) :
    """Implement Plan Subscribe for authenticated users"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckoutSerializer
