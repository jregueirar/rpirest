from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import Task, Pixel, XY

STATUSES = (
    'New',
    'Ongoing',
    'Done',
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class XYSerializer(serializers.Serializer):
    x = serializers.IntegerField(min_value=0, max_value=7);
    y = serializers.IntegerField(min_value=0, max_value=7);


class PixelSerializer(XYSerializer):
    r = serializers.IntegerField(min_value=0, max_value=255);
    g = serializers.IntegerField(min_value=0, max_value=255);
    b = serializers.IntegerField(min_value=0, max_value=255);

    class Meta:
        model = Pixel
        fields = ('url', 'x', 'y', 'r', 'g', 'b')
    #def create(self, validated_data):
    #    return Pixel(id=None, **validated_data)

    # def update(self, instance, validated_data):
    #     for field, value in validated_data.items():
    #         setattr(instance, field, value)
    #     return instance

