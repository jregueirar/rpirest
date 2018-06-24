# Create your views here.
import logging

import psutil
from rest_framework import viewsets, status
from rest_framework.response import Response

from .tasks import play_audio
from core.common import MyRouter
from core.common import apirest_response_format
from .serializers import SoundSerializer
from celery.result import AsyncResult



def routes():
    router = MyRouter()
    router.register(r'cpu', CPUPercentView, base_name='rpi_cpu')
    router.register(r'memory', MemoryView, base_name='rpi_memory')
    router.register(r'mountpoints', DiskPartitionView, base_name='rpi_disk_partition')
    router.register(r'mountpoints-usage', DiskUsageView, base_name='rpi_disk_usage')
    router.register(r'audio', SoundView, base_name='audio')
    router.register(r'taskinfo',TaskView, base_name='task' )
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
    def list(self, request):

        data=psutil.cpu_percent(interval=1, percpu=True)
        response = apirest_response_format(url=request.path,
                                           status="success",
                                           msg="Percents per CPU",
                                           result=data)
        return Response(response)

class MemoryView(viewsets.ViewSet):
    """
    Return statistics about system memory usage.
    More info: http://psutil.readthedocs.io/en/latest/#memory
    """
    def list(self, request):

        data=psutil.virtual_memory()
        msg_out="Memory Statistics"
        response = apirest_response_format(url=request.path, status="success", msg=msg_out, result=data._asdict())
        return Response(response)

class DiskPartitionView(viewsets.ViewSet):
    """
    Return all mounted disk partitions as a list of named tuples including device, mount
    point and filesystem type, similarly to “df” command on UNIX
    """
    def list(self, request):
        data=psutil.disk_partitions()
        result=[]
        for i in data:
            result.append(i._asdict())
        msgOut="List of all mounted partitions"
        response = apirest_response_format(url=request.path, status="success", msg=msgOut, result=result)
        return Response(response)

class DiskUsageView(viewsets.ViewSet):
    """
    Return disk usage statistics of all mount points.
    """
    def list(self, request):
        partitions = psutil.disk_partitions()
        data = []
        for partition in partitions:
            aux = {}
            aux[partition.mountpoint] = psutil.disk_usage(partition.mountpoint)._asdict()
            data.append(aux);
        # data=psutil.disk_usage(mount_point)._asdict()
        msgOut="Use of mount points"
        response = apirest_response_format(url=request.path, status="SUCCESS", msg=msgOut, result=data)
        return Response(response)

class SoundView(viewsets.ViewSet):
    """
    Reproduce or return a list of sounds.
    """
    serializer_class = SoundSerializer

    def update(self, request):
        serializer = SoundSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            task = play_audio.delay(1, serializer.data['sound_path'])
            msgOut="Testing"
            response = apirest_response_format(request.path,
                                               status=task.status,
                                               msg=msgOut,
                                               result="Reproducing audio " + serializer.data['sound_path'],
                                               jobid=task.id)
            return Response(response)



class TaskView(viewsets.ViewSet):
    """
    Show the status of one Asyncronous Task.
    PK = Task Id.
    """
    def retrieve(self, request, pk=None):
        if pk is not None:
            response = apirest_response_format( request.path,
                                                status=AsyncResult(pk).status,
                                                msg="Status of the asyncronous task",
                                                result=AsyncResult(pk).status,
                                                jobid=pk,
                                                )
            return Response(response)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # def list(self, request):
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
