from rest_framework.generics import CreateAPIView
from users.apis.serializers.register import RegisterSerializer

class UserRegisterAPI (CreateAPIView) : 
    serializer_class = RegisterSerializer
    