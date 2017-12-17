# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework import viewsets, status
from apirest.serializers import *
from rest_framework.decorators import detail_route, list_route
#from sense_hat import SenseHat
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django.core.files.storage import default_storage as storage
from .utils import save_uploaded_file_to_disk
from django.conf import settings
from core.common import apirest_response_format
import logging

# Get an instance of a logger
logger = logging.getLogger("apirest")
logger.debug("IS_RPI: " + str(settings.IS_RPI))

# Useful for testing. For example: Deployments in docker or vagrant
if settings.IS_RPI:
    try:
        from sense_hat import SenseHat
    except ImportError:
        raise SystemExit('[ERROR] Please make sure sense_hat is installed properly')

    # Parche para permitir despliegue sin que sensehat este conectado
    # Fixme: ¿mejorar para que se vea el error en la APP web?
    # Si no se pone la excepción falla el despliegue si el sense-hat no está enchufado
    try:
        logger.debug("Initializing sense")
        sense = SenseHat()
    except OSError:
        logger.error("[ERROR] Initializing sensehat. Please make sure sense_hat is installed properly")
        # Escribimos en base de datos status o en el render...¿Decorador para cada vista?.
        pass


class APIRoot(APIView):

    def get(self, request):
        # Assuming we have views named 'foo-view' and 'bar-view'
        # in our project's URLconf.
        return Response({
            'foo': reverse('PixelView', request=request)
        })

###########
# LED MATRIX
###########
# RESPONSE FORMAT: http://labs.omniti.com/labs/jsend/wiki
class RotationView(viewsets.ViewSet):
    """
    If you're using the Pi upside down or sideways you can use this function to correct the orientation of the image being shown.

    Parameter; Type; Valid values;Explanation

    r; Integer; 0 90 180 270; The angle to rotate the LED matrix though. 0 is with the Raspberry Pi HDMI port facing downwards.

    redraw; Boolean; True False; Whether or not to redraw what is already being displayed on the LED matrix. Defaults to True
    """
    serializer_class = AngleSerializer

    def update(self, request, pk=None):
        serializer = AngleSerializer(data=request.data)
        if serializer.is_valid():
            logger.debug("Redraw: " + str(serializer.data['redraw']))
            sense.set_rotation(serializer.data['angle'], serializer.data['redraw'])
            response = {}
            response['status'] = "success"
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Voltear Horizontalmente: https://docs.gimp.org/es/gimp-layer-flip-horizontal.html
class FlipHView(viewsets.ViewSet):
    serializer_class = RedrawSerializer

    def update(self, request, pk=None):
        serializer = RedrawSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = {'status': 'success'}
            response['data'] = {'pixel_list': sense.flip_h(serializer.data['redraw'])}
            return Response(response, status=status.HTTP_200_OK)


# ¿Ponemos en data el atributo redraw?
# https://docs.gimp.org/es/gimp-layer-flip-vertical.html
class FlipVView(viewsets.ViewSet):
    serializer_class = RedrawSerializer

    def update(self, request, pk=None):
        serializer = RedrawSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = {'status': 'success'}
            response['data'] = {'pixel_list': sense.flip_v(serializer.data['redraw'])}
            return Response(response, status=status.HTTP_200_OK)


class LoadImageView(viewsets.ViewSet):
    serializer_class = ImageSerializer


    def update(self, request, pk=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            path = save_uploaded_file_to_disk("/tmp/img.png", request.FILES['img'])
            response = {'status': 'success'}
            response['data'] = {'pixel_list': sense.load_image(path)}
            return Response(response, status=status.HTTP_200_OK)


class ClearView(viewsets.ViewSet):
    serializer_class = ColorSerializer

    def update(self, request, pk=None):
        serializer = ColorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            sense.clear(serializer.data['r'], serializer.data['g'], serializer.data['b'])
            response = {'status': 'success'}
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_200_OK)

def hash_colour_2_list(hash):
    return [hash['r'], hash['g'], hash['b']];

class ShowMessageView(viewsets.ViewSet):
    """
    Scrolls a text message from right to left across the LED matrix and at
    the specified speed, in the specified colour and background colour.
    """
    serializer_class = MessageSerializer

    def update(self, request, pk=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            sense.show_message(request.data['text_string'],
                                scroll_speed=serializer.data['scroll_speed'],
                                text_colour=hash_colour_2_list(serializer.data['text_colour']),
                                back_colour=hash_colour_2_list(serializer.data['back_colour'])
                               )
            response = {'status': 'success'}
            response['url'] = request.path
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_200_OK)

class ShowLetterView(viewsets.ViewSet):
    serializer_class = LetterSerializer

    def update(self, request, pk=None):
        serializer = LetterSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            sense.show_letter(serializer.validated_data['letter'],
                              text_colour=hash_colour_2_list(serializer.data['text_colour']),
                              back_colour=hash_colour_2_list(serializer.data['back_colour'])
                              )
            response = {'status': 'success'}
            response['url'] = request.path
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_200_OK)

class LowLightView(viewsets.ViewSet):
    """
    Toggles the LED matrix low light mode,
    useful if the Sense HAT is being used in a dark environment.
    """
    serializer_class = LowLightSerializer

    def update(self, request, pk=None):
        self.serializer_class = LowLightSerializer
        serializer = LowLightSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            sense.low_light = serializer.data['low_light']
            response = {'status': 'success'}
            response['url'] = request.path   # FIXME ¿Redundante? ¿Lo dejamos?. Crear un formato de respuesta unico.
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_200_OK)


class GammaView(viewsets.ViewSet):
    """
    For advanced users. Most users will just need the low_light Boolean property
    above. The Sense HAT python API uses 8 bit (0 to 255) colours for R, G, B.
    When these are written to the Linux frame buffer they're bit shifted into RGB 5 6 5.
    The driver then converts them to RGB 5 5 5 before it passes them over to the
    ATTiny88 AVR for writing to the LEDs.

    The gamma property allows you to specify a gamma lookup table for the final 5 bits
    of colour used. The lookup table is a list of 32 numbers that must be between 0 and 31.
    The value of the incoming 5 bit colour is used to index the lookup table and the value
    found at that position is then written to the LEDs.
    """

    def list(self, request):

        response={'url': request.path}
        response['status']='success'
        response['data'] = {'gamma_tuple': sense.gamma}
        return Response(response)

    def update(self, request, pk=None):
        serializer = GammaSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            sense.gamma = serializer.data['gamma_tuple']
            response = {'status': 'success'}
            response['url'] = request.path   # FIXME ¿Redundante? ¿Lo dejamos?
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        sense.gamma_reset()
        response = {'status': 'success'}
        response['url'] = request.path
        response['data'] = {'gamma_tuple': sense.gamma}
        return Response(response)

class HumidityView(viewsets.ViewSet):
    """
    Gets the current percent of humidity from the humidity sensor.
    """
    def list(self, request):
        result = sense.get_humidity()
        response = apirest_response_format(request.path, "success", "Humidity (%)", result)
        return Response(response)


        response={'url': request.path}
        response['status']="success"
        response['msg'] = "Sensor Sense Hat "
        response['result'] = result
        return Response(response)


class TemperatureView(viewsets.ViewSet):
    """
    Gets the current temperature in degrees Celsius from the humidity sensor.
    Api rest of get_temperature_from_humidity.
    [ref]: https://pythonhosted.org/sense-hat/api/#environmental-sensors
    """

    def list(self, request):
        result = sense.get_temperature_from_humidity()
        response = apirest_response_format(request.path, "success", "Temperature in degrees Celsius", result)
        logger.debug('TemperatureView: ' + str(result))
        return Response(response)

class TemperatureFromHumidityView(viewsets.ViewSet):
    """
    https://pythonhosted.org/sense-hat/api/#environmental-sensors
    Gets the current temperature in degrees Celsius from the humidity sensor.
    """

    def list(self, request):
        result = sense.get_temperature_from_humidity()
        response={'url': None}
        response['Temperature'] = result
        return Response(response)


class TemperatureFromPressureView(viewsets.ViewSet):
    """
    Gets the current temperature in degrees Celsius from the humidity sensor.
    """

    def list(self, request):
        result = sense.get_temperature_from_pressure()
        response = apirest_response_format(request.path, "success", "Temperature in degrees Celsius", result)
        return Response(response)



class PressureView(viewsets.ViewSet):
    """
    https://pythonhosted.org/sense-hat/api/#environmental-sensors
    Gets the current temperature in degrees Celsius from the humidity sensor.
    """

    def list(self, request):
        result = sense.get_pressure()
        response=apirest_response_format(request.path, "success", "Pressure", result)
        return Response(response)


class PixelView(viewsets.ViewSet):
    """
        Set/Get the color of an individual LED matrix pixel at the specified X-Y coordinate.
    """
    serializer_class = ColorSerializer
    lookup_value_regex = '[0-7],[0-7]'

    def list(self, request):
        self.serializer_class = PixelSerializer
        serializer = XYSerializer(data=request.data)
        if serializer.is_valid():
            coordinate = serializer.data
            color = sense.get_pixel(coordinate['x'], coordinate['y'])
            pixel = {}
            pixel['color'] = {
                        'r': color[0],
                        'g': color[1],
                        'b': color[2]
                        }
            pixel['coord'] = {
                'x': coordinate['x'],
                'y': coordinate['y']
            }
            return Response({'pixel': pixel})
        errors=serializer.errors
        errors['URL'] = "Prueba con"
        return Response(errors)


    """
        Function: sense_hat.set_pixel
    """
    def update(self, request, pk=None):

        serializer=PixelSerializer(data=request.data)
        if serializer.is_valid():
            sense.set_pixel(serializer.data['x'],
                            serializer.data['y'],
                            serializer.data['r'],
                            serializer.data['g'],
                            serializer.data['b'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_element(self, request, pk=None):
        x, y = pk.split(sep=",")
        serializer = XYSerializer(data={'x': int(x), 'y': int(y)})
        serializer.is_valid(raise_exception=True)

        request.data['x'] = int(x)
        request.data['y'] = int(y)
        serializer=PixelSerializer(data=request.data)
        if serializer.is_valid():
            sense.set_pixel(serializer.data['x'],
                            serializer.data['y'],
                            serializer.data['r'],
                            serializer.data['g'],
                            serializer.data['b'])
            response={'update_element': "YES"};
            serializer.data['url'] = None
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        print ("Retrieve")
        if pk is not None:
            x, y = pk.split(sep=",")
            serializer = XYSerializer(data={'x': int(x), 'y': int(y)})
            if serializer.is_valid():
                data = serializer.data
                color = sense.get_pixel(data['x'], data['y'])
                response = {};
                response['pixel'] = {
                                    'color': {
                                        'r': color[0],
                                        'g': color[1],
                                        'b': color[2]
                                        },
                                    'coord': {'x': int(x), 'y': int(y)}
                                    }
                response['url'] = None
                return Response(response, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # FIXME: No funciona
    def metadata(self, request):
        """
        Don't include the view description in OPTIONS responses.
        """
        data = super(PixelView, self).metadata(request)
        data.pop('description')
        # data.add({"tutua":'probando'})
        return data


class PixelsView(viewsets.ViewSet):
    lookup_value_regex = '[0-7],[0-7]'
    serializer_class = ColorSerializer

    def get_queryset(self):
        pixel_list = sense.get_pixels()
        queryset_list = []

        i = 0
        for pixel_color in pixel_list:
            coordinates = Pixel.get_coordinates(i)

            queryset_list.append(Pixel(x=coordinates['x'], y=coordinates['y'],
                                       r=pixel_color[0],
                                       g=pixel_color[1],
                                       b=pixel_color[2]))
            i += 1

        return queryset_list

    #def list(self, request):
    #    queryset = self.get_queryset()
    #    serializer = PixelSerializer(queryset, many=True)
    #    return Response(serializer.data)

    def list(self, request):
        self.serializer_class=None

        pixel_list = sense.get_pixels()
        return Response({"pixel_list": pixel_list})

    def retrieve(self, request, pk=None):
        print ("Retrieve")
        if pk is not None:
            x, y = pk.split(sep=",")
            serializer = XYSerializer(data={'x': int(x), 'y': int(y)})
            if serializer.is_valid():
                data = serializer.data
                color = sense.get_pixel(data['x'], data['y'])
                response = {};
                response['pixel'] = {
                                    'color': {
                                        'r': color[0],
                                        'g': color[1],
                                        'b': color[2]
                                        },
                                    'coord': {'x': int(x), 'y': int(y)}
                                    }
                response['url'] = None
                return Response(response, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        self.serializer_class = None

        # TODO Check validation
        serializer = PixelSerializer(data=request.data, many=True)
        pixel_list = request.data['pixel_list']
        i=0
        for pixel in pixel_list:
            coordinates = Pixel.get_coordinates(i)
            print("x,y ->" + str(coordinates['x']) + "," + str(coordinates['y']))
            validate_pixel = PixelSerializer(data={'x': coordinates['x'],
                                                   'y': coordinates['y'],
                                                   'r': pixel[0],
                                                   'g': pixel[1],
                                                   'b': pixel[2]
                                                   }
                                             )
            validate_pixel.is_valid(raise_exception=True)
            i += 1

        sense.set_pixels(pixel_list)
        return Response({'pixel_list': pixel_list})

    """
        Function: sense_hat.set_pixel
    """
    def update_element(self, request, pk=None):
        self.serializer_class = ColorSerializer;

        x, y = pk.split(sep=",")
        serializer = XYSerializer(data={'x': int(x), 'y': int(y)})
        serializer.is_valid(raise_exception=True)

        request.data['x'] = int(x)
        request.data['y'] = int(y)
        serializer=PixelSerializer(data=request.data)
        if serializer.is_valid():
            sense.set_pixel(serializer.data['x'],
                            serializer.data['y'],
                            serializer.data['r'],
                            serializer.data['g'],
                            serializer.data['b'])
            response={'update_element': "YES"};
            serializer.data['url'] = None
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImuConfigView(viewsets.ViewSet):
    """
    Enables and disables the gyroscope, accelerometer and/or magnetometer
    contribution to the get orientation functions below.
    """
    serializer_class = ImuConfigSerializer

    def update(self, request, pk=None):
        serializer=ImuConfigSerializer(data=request.data)
        if serializer.is_valid():
            sense.set_imu_config(
                serializer.data['compass_enabled'],
                serializer.data['gyro_enabled'],
                serializer.data['accel_enabled']
                )
            response={'status': 'success'}
            response['path'] = request.path
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrientationRadiansView(viewsets.ViewSet):
    """
    Gets the current orientation in radians using the aircraft principal axes
    of pitch, roll and yaw.
    """
    def list(self, request, pk=None):
        response={'status': 'success'}
        response['url'] = request.path
        response['data'] = sense.get_orientation_radians()
        return Response(response)


class OrientationDegreesView(viewsets.ViewSet):
    """
    Gets the current orientation in degrees using the aircraft principal axes
    of pitch, roll and yaw.
    """
    def list(self, request, pk=None):
        response={'status': 'success'}
        response['url'] = request.path
        response['data'] = sense.get_orientation_degrees()
        return Response(response)


class CompassView(viewsets.ViewSet):
    """
    Calls set_imu_config to disable the gyroscope and accelerometer then gets
    the direction of North from the magnetometer in degrees.
    """
    def list(self, request, pk=None):
        response={'status': 'success'}
        response['url'] = request.path
        response['data'] = sense.get_compass()
        return Response(response)


class CompassRawView(viewsets.ViewSet):
    """
    Gets the raw x, y and z axis magnetometer data.
    """
    def list(self, request, pk=None):
        response={'status': 'success'}
        response['url'] = request.path
        response['data'] = sense.get_compass_raw()
        return Response(response)


class GyroscopeView(viewsets.ViewSet):
    """
    Calls set_imu_config to disable the magnetometer and accelerometer then
    gets the current orientation from the gyroscope only.
    """
    def list(self, request, pk=None):
        response={'status': 'success'}
        response['url'] = request.path
        response['data'] = sense.get_gyroscope()
        return Response(response)

class GyroscopeRawView(viewsets.ViewSet):
    """
    Gets the raw x, y and z axis gyroscope data.
    """
    def list(self, request, pk=None):
        response={'status': 'success'}
        response['url'] = request.path
        response['data'] = sense.get_gyroscope_raw()
        return Response(response)


class AccelerometerView(viewsets.ViewSet):
    """
    Calls set_imu_config to disable the magnetometer and gyroscope
    then gets the current orientation from the accelerometer only.
    """
    def list(self, request, pk=None):
        response={'status': 'success'}
        response['url'] = request.path
        response['data'] = sense.get_accelerometer()
        return Response(response)


class AccelerometerRawView(viewsets.ViewSet):
    """
    Gets the raw x, y and z axis accelerometer data.
    """
    def list(self, request, pk=None):
        response={'status': 'success'}
        response['url'] = request.path
        response['data'] = sense.get_accelerometer_raw()
        return Response(response)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @list_route()
    @detail_route(methods=['post'])
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


from rest_framework import authentication, permissions
from rest_framework.views import APIView

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
