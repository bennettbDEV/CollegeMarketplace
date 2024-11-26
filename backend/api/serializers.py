#api/serializers.py
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from api.authentication import validate_user_credentials


# Authentication serializer - CustomTokenObtainPairSerializer
class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        user = validate_user_credentials(username, password)

        if user is None:
            raise AuthenticationFailed("Invalid credentials.")
        return attrs


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)  # Wont be revealed in reads
    location = serializers.CharField(max_length=50, allow_null=True)


class ListingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    condition = serializers.ChoiceField(choices=["Factory New", "Minimal Wear", "Fair", "Well Worn", "Refurbished"])
    description = serializers.CharField(max_length=500)
    price = serializers.FloatField()
    image = serializers.ImageField(use_url=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)
    tags = serializers.ListField(allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    author_id = serializers.IntegerField(read_only=True)

    # When fetching serialized data - turn image field into url reference
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image = instance.get("image")
        if image:
            representation["image"] = image
        return representation

    """
    def validate(self, attrs):
        if not attrs.get("title"):
            raise serializers.ValidationError("Title is required.")
        if not attrs.get("description"):
            raise serializers.ValidationError("Description is required.")
        return attrs"""
