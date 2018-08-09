from rest_framework import serializers

class DelaySerializer(serializers.Serializer):
    time = serializers.IntegerField(default=10)
