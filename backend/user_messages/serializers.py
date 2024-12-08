from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sender_id = serializers.IntegerField(read_only=True)
    receiver_id = serializers.IntegerField(allow_null=False)
    content = serializers.CharField(max_length=200, allow_null=False)
