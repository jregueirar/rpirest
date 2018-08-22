from rest_framework import serializers

class MPDSerializer(serializers.Serializer):
    position = serializers.IntegerField()
