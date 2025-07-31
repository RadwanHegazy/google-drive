from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from users.models import User
from file.models import UserFile

class ShareFileSerializer (serializers.Serializer) : 
    file = serializers.PrimaryKeyRelatedField(
        queryset = UserFile.objects.all()
    )
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = User.objects.all()
    )

    def validate(self, attrs):
        file : UserFile = attrs.get('file')
        request = self.context.get('request')

        # check if owner
        if request.user != file.owner : 
            raise  PermissionDenied({
                'message' : "not authorized"
            })
        
        return attrs
    
    def create(self, validated_data):
        file : UserFile = validated_data.get('file')
        users : list[User] = validated_data.get('users')
        users += file.shared_with.all()
        file.shared_with.set(users)
        file.save()
        return file
    
    def to_representation(self, instance):
        return {
            'message' : "operation done successfully"
        }
    

class RemoveFromSharedSerializer (serializers.Serializer) : 
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = User.objects.all()
    )
    