from rest_framework.views import APIView
from rest_framework import status, response, permissions
from plan.models import StoragePlan
from django.shortcuts import get_object_or_404
from plan.utlities import create_stripe_checkout_link

class UserPlanSubscribe (APIView) :
    """Implement Plan Subscribe for authenticated users"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, plan_id) : 
        plan = get_object_or_404(StoragePlan, id=plan_id)
        user = self.request.user
        checkout_url = create_stripe_checkout_link(user)
        return response.Response({
            'url' : checkout_url
        }, status=status.HTTP_200_OK)