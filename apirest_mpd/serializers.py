from rest_framework import serializers

class MPDSerializer(serializers.Serializer):
    pos = serializers.IntegerField()
