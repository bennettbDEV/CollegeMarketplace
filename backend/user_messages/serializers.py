from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sender = serializers.IntegerField(read_only=True)
    receiver = serializers.IntegerField(read_only=True)
    content = serializers.CharField(max_length=200, allow_null=False)
