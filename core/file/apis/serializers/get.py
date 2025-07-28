from rest_framework import serializers
from file.models import UserFile
from users.apis.serializers.profile import ProfileSerializer

class ListUserFileSerializer (serializers.ModelSerializer) : 
    
    class Meta:
        model = UserFile
        fields = [
            'id',
            'name',
            'created_at',
            'updated_at',
            'file_size_in_giga',
        ]

class RetrieveUserFileSerializer (serializers.ModelSerializer) : 
    owner = ProfileSerializer()
    shared_with = ProfileSerializer(many=True)
    
    class Meta:
        model = UserFile
        fields = "__all__"