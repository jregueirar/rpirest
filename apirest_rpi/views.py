# Create your views here.
import logging

import psutil
from rest_framework import viewsets, status
from rest_framework.response import Response

from .tasks import play_audio, sync_job_db
from core.common import MyRouter
from core.common import apirest_response_format
from core.models import Job
from .serializers import SoundSerializer


def routes():
    router = MyRouter()
    router.register(r'cpu', CPUPercentView, base_name='rpi_cpu')
    router.register(r'memory', MemoryView, base_name='rpi_memory')
    router.register(r'mountpoints', DiskPartitionView, base_name='rpi_disk_partition')
    router.register(r'mountpoints-usage', DiskUsageView, base_name='rpi_disk_usage')


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
        response = apirest_response_format(request=request,
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
        response = apirest_response_format(request=request, status="success", msg=msg_out, result=data._asdict())
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
        response = apirest_response_format(request=request, status="success", msg=msgOut, result=result)
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
        response = apirest_response_format(request=request, status="SUCCESS", msg=msgOut, result=data)
        return Response(response)

class SoundView(viewsets.ViewSet):
    """
    Reproduce or return a list of sounds.
    """
    serializer_class = SoundSerializer

    def update(self, request):
        serializer = SoundSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            task = play_audio.delay(serializer.data['sound_path'])
            job = Job(
                name="play_audio",
                celery_id= task.id
            )
            job.save()
            # FIXME sync_job_db
            #play_audio.apply_async(serializer.data['sound_path'], job.id, link=sync_job_db.s())
            # (play_audio.s(serializer.data['sound_path'], job.id) | sync_job_db.s(job.id)).delay()

            msg_out="Asyncronous task. play_audio: " + serializer.data['sound_path']
            response = apirest_response_format(request=request,
                                               status=task.status,
                                               msg=msg_out,
                                               result="",
                                               job_id=job.id,
                                               )
            return Response(response)
