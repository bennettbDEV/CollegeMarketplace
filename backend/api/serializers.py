# api/serializers.py
"""
CLASSES:
LoginSerializer, UserSerializer, ListingSerializer
"""

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.authentication import CustomJWTAuthentication


# Authentication serializer
class LoginSerializer(TokenObtainPairSerializer):
    """Serializer class for handling user login and token generation.

    This serializer extends 'TokenObtainPairSerializer' and is responsible
    for validating user credentials (username and password) and generating JWT tokens
    for successful login. It ensures that the user provides valid credentials before
    issuing a token. If the credentials are invalid, an 'AuthenticationFailed' error is raised.
    """

    def validate(self, attrs):
        """Validate the provided credentials (username and password).

        This method checks if the provided username and password match the credentials of an
        existing user. If valid, the method allows the token generation to proceed. Otherwise,
        it raises an 'AuthenticationFailed' exception.

        Args:
            attrs (dict): A dictionary containing the username and password provided by the user.

        Returns:
            dict: The validated attributes (username and password), which will be used for token generation.

        Raises:
            AuthenticationFailed: If the credentials are invalid or do not match any user.
        """

        username = attrs["username"]
        password = attrs["password"]

        user = CustomJWTAuthentication.validate_user_credentials(username, password)

        if user is None:
            raise AuthenticationFailed("Invalid credentials.")
        return attrs


class UserSerializer(serializers.Serializer):
    """Serializer class for handling user data representation and validation.

    This serializer is responsible for validating and serializing user data. It provides
    a way to represent the user model data for both reading and writing to the API.

    Note:
        When submitting an image, make sure the request is sent with the 'Content-Type' header as 'multipart/form-data'.

    Attributes:
        id (IntegerField): The unique identifier of the user. Read-only.
        username (CharField): The username of the user. Maximum length is 50 characters.
        password (CharField): The password of the user. Write-only, not included in read operations.
        location (CharField): The location of the user. Allows null. Defaults to empty string.
        email (EmailField): The email address of the user. Allows null. Defaults to None.
        image (ImageField): The image associated with the user. Allows null. Defaults to None.
    """

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)  # Wont be revealed in reads
    location = serializers.CharField(max_length=50, allow_null=True, default="")
    email = serializers.EmailField(allow_null=True, default=None)
    image = serializers.ImageField(use_url=True, allow_null=True, default=None)

    def to_representation(self, instance):
        """Override the default representation method to include the image URL in the serialized data.

        Args:
            instance (User): The instance of the user model to serialize.

        Returns:
            dict: The serialized representation of the user, including the image URL if present.
        """

        # When fetching serialized data - turn image field into url reference
        representation = super().to_representation(instance)
        image = instance.image
        if image:
            representation["image"] = image
        return representation


class ListingSerializer(serializers.Serializer):
    """Serializer class for handling listing data representation and validation.

    This serializer is responsible for validating and serializing listing data. It provides
    a way to represent the listing model data for both reading and writing to the API.

    Note:
        When submitting an image, make sure the request is sent with the 'Content-Type' header as 'multipart/form-data'.

    Fields:
        id (IntegerField): The unique identifier of the listing. Read-only.
        title (CharField): The title of the listing. Maximum length is 50 characters.
        condition (ChoiceField): The condition of the item being listed.
                                Choices are: Factory New, Minimal Wear, Fair, Well Worn, Refurbished.
        description (CharField): A description of the listing. Maximum length is 500 characters.
        price (FloatField): The price of the item being listed.
        image (ImageField): The image associated with the listing, represented as a URL.
        likes (IntegerField): The number of likes the listing has received. Read-only.
        dislikes (IntegerField): The number of dislikes the listing has received. Read-only.
        tags (ListField): A list of tags associated with the listing. Allows null.
        created_at (DateTimeField): The timestamp when the listing was created. Read-only.
        author_id (IntegerField): The ID of the user who created the listing. Read-only.

    Methods:
        to_representation(instance):
            Customizes the representation of the serialized data by converting the image field into a URL.
            This method is called when fetching serialized data for a listing.
    """

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    condition = serializers.ChoiceField(
        choices=["Factory New", "Minimal Wear", "Fair", "Well Worn", "Refurbished"]
    )
    description = serializers.CharField(max_length=500)
    price = serializers.FloatField()
    image = serializers.ImageField(use_url=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)
    tags = serializers.ListField(allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    author_id = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        """Override the default representation method to include the image URL in the serialized data.

        Args:
            instance (Listing): The instance of the listing model to serialize.

        Returns:
            dict: The serialized representation of the listing, including the image URL.
        """

        representation = super().to_representation(instance)
        image = instance.image
        if image:
            representation["image"] = image
        return representation