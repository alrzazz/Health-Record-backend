from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
