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
    r = serializers.IntegerField(min_value=0, max_value=255, default=0, help_text="Optional. Values range between 0 and 255. Default 0.")
    g = serializers.IntegerField(min_value=0, max_value=255, default=0, help_text="Optional. Values range between 0 and 255. Default 0.")
    b = serializers.IntegerField(min_value=0, max_value=255, default=0, help_text="Optional. Values range between 0 and 255. Default 0.")


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

# Fixme Improve validator TexColour, error message,..
# http://www.django-rest-framework.org/topics/html-and-forms/#rendering-forms, ¿Mejorarlo?.
#   Limit the list field to 3 elements.
class TextCommonSerializer(serializers.Serializer):
    text_colour = ColorSerializer(help_text="Optional")
    back_colour = ColorSerializer()

        # serializers.ListField(child=serializers.IntegerField(default=0, min_value=0, max_value=255),
        #                                 min_length=3,
        #                                 max_length=3,
        #                                 default=[255, 255, 255],
        #                                 help_text="Optional. Default [255,255,255]",
        #                                 style={'base_template': 'list_fieldset.html'}
        #                                 )
    # back_colour = serializers.ListField(child=serializers.IntegerField(min_value=0, max_value=255),
    #                                     min_length=3,
    #                                     max_length=3,
    #                                     default=[0, 0, 0],
    #                                     help_text="Optional",
    #                                     style={'base_template': 'list_fieldset.html'})


class LetterSerializer(TextCommonSerializer):
    letter = serializers.CharField(allow_null=False, max_length=1, help_text="The letter to show.")


class MessageSerializer(TextCommonSerializer):
    text_string = serializers.CharField()
    scroll_speed= serializers.FloatField(default=0.1)




class LowLightSerializer(serializers.Serializer):
    low_light = serializers.BooleanField(default=False)


class GammaSerializer(serializers.Serializer):
    gamma_tuple = serializers.ListField(child=serializers.IntegerField(min_value=0, max_value=255), default=[255,255,255])

class ImuConfigSerializer(serializers.Serializer):
    compass_enabled = serializers.BooleanField()
    gyro_enabled = serializers.BooleanField()
    accel_enabled = serializers.BooleanField()

