# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework import viewsets
#from apirest_sensehat.serializers import *
from django.conf import settings
from core.common import MyRouter
from core.common import apirest_response_format
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

import logging


def routes():

    router = MyRouter()
    router.register(r'env_sensor/humidity', HumidityView, base_name='dht_humidity')
    router.register(r'env_sensor/temperature', TemperatureView, base_name='dht_temperature')
    return router.urls



if settings.IS_RPI:
    try:
        import Adafruit_DHT

        DHT_SENSORS = {'dht11': Adafruit_DHT.DHT11,
                        'dht22': Adafruit_DHT.DHT22,
                        'am2302': Adafruit_DHT.AM2302
                      }
    except ImportError:
        raise SystemExit('[ERROR] Please make sure Adafruit_DHT is installed properly')

# Get an instance of a logger
logger = logging.getLogger("apirest_dht")

# def is_rpi_system(request):
#
#     response = {'url': request.path}
#     response['status'] = "error"
#     response['msg'] = "[ERROR] Please make sure Adafruit_DHT is installed properly"
#     return Response(response)


# Create your views here.
# class HumidityView(viewsets.ViewSet):

# A single entry point to the API. A index.

# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'humidity': reverse('HumidityView', request=request, format=format)
#     })

# class APIRoot(APIView):
#
#     def get(self, request):
#         return Response({
#             'HumidityView': reverse('HumidityView', request=request)
#         })

class HumidityView(viewsets.ViewSet):
    """
    Gets the current temperature in degrees Celsius from the humidity sensor.
    """
    # Device is from urls.py: am2302, dht11 or dht22
    def list(self, request, device):
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSORS[device], settings.DHT_GPIO_PIN)
        logger.debug('HumidityView: ' + str(humidity))
        response = apirest_response_format(request=request, status="success", msg="Sensor " + device, result=humidity)
        return Response(response)

class TemperatureView(viewsets.ViewSet):
    """
    Gets the current temperature in degrees Celsius from the humidity sensor.
    Api rest of get_temperature_from_humidity.
    [ref]: https://pythonhosted.org/sense-hat/api/#environmental-sensors
    """
    def list(self, request, device):
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSORS[device], settings.DHT_GPIO_PIN)
        response = apirest_response_format(request=request, status="success", msg="Sensor " + device, result=temperature)
        return Response(response)


