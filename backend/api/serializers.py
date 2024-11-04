from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)  # Wont be revealed in reads
    location = serializers.CharField(max_length=50)

    def validate(self, attrs):
        pass

class ListingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=500)
    price = serializers.FloatField()
    created_at = serializers.DateTimeField(read_only=True)
    # maybe change write_only for author_id
    author_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        if not attrs.get("title"):
            raise serializers.ValidationError("Title is required.")
        if not attrs.get("description"):
            raise serializers.ValidationError("Description is required.")
        return attrs
