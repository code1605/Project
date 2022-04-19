from rest_framework import serializers


class PayloadSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, max_length=255, label="Text Body")

    def create(self, validated_data):
        return PayloadSerializer(**validated_data)