from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer (
    serializers.ModelSerializer
) : 
    
    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'password'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)