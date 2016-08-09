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
    x = serializers.IntegerField(min_value=0, max_value=7)
    y = serializers.IntegerField(min_value=0, max_value=7)


class ColorSerializer(serializers.Serializer):
    r = serializers.IntegerField(min_value=0, max_value=255, default=0)
    g = serializers.IntegerField(min_value=0, max_value=255, default=0)
    b = serializers.IntegerField(min_value=0, max_value=255, default=0)


class PixelSerializer(XYSerializer):
    r = serializers.IntegerField(min_value=0, max_value=255, default=0)
    g = serializers.IntegerField(min_value=0, max_value=255, default=0)
    b = serializers.IntegerField(min_value=0, max_value=255, default=0)

    class Meta:
        model = Pixel
        fields = ('url', 'x', 'y', 'r', 'g', 'b')


class RedrawSerializer(serializers.Serializer):
    redraw = serializers.BooleanField(default=True)


class AngleSerializer(RedrawSerializer):
    angle = serializers.ChoiceField(choices=[0, 90, 180, 270])

class ImageSerializer(RedrawSerializer):
    img = serializers.ImageField()
