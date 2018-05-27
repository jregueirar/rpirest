# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets
from core.common import MyRouter
from core.common import apirest_response_format
import psutil
import logging


def routes():
    router = MyRouter()
    router.register(r'cpu', CPUPercentView, base_name='rpi_cpu')
    #router.register(r'memory', TemperatureView, base_name='dht_temperature')
    return router.urls

# Get an instance of a logger
logger = logging.getLogger("apirest_rpì")

class CPUPercentView(viewsets.ViewSet):
    """
    Returns a list of floats representing the
    utilization as a percentage for each CPU.
    First element of the list refers to first CPU, second element
    to second CPU and so on.
    """
    # Device is from urls.py: am2302, dht11 or dht22
    def list(self, request):

        data=psutil.cpu_percent(interval=1, percpu=True)
        response = apirest_response_format(url=request.path, status="success", msg="Percents per CPU", result=data)
        return Response(response)
