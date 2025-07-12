from rest_framework import serializers
from plan.models import StoragePlan

class StoragePlanSerializer (serializers.ModelSerializer) : 

    class Meta:
        model = StoragePlan
        fields = "__all__"