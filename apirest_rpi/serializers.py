from rest_framework import serializers

class SoundSerializer(serializers.Serializer):
    sound_path = serializers.CharField()
