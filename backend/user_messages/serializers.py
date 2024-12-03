from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from api.authentication import validate_user_credentials

class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sender = serializers.IntegerField(read_only=True)
    receiver = serializers.IntegerField(read_only=True)
    content = serializers.CharField(max_length=200, allow_null=False)