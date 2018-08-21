import logging

import psutil
from rest_framework import viewsets, status
from rest_framework.response import Response

from core.common import MyRouter
from core.common import apirest_response_format
from core.models import Job
from .serializers import MPDSerializer
import mpd
from contextlib import contextmanager

HOST, PORT = '127.0.0.1', 6600
client = mpd.MPDClient()

@contextmanager
def connection():
    try:
        client.connect(HOST, PORT)
        yield
    finally:
        client.close()
        client.disconnect()



def routes():
    router = MyRouter()
    router.register(r'play', PlayView, base_name='mpd_play')
    router.register(r'stop', StopView, base_name='stop_play')
    # router.register(r'list', ListView, base_name='list_play')
    return router.urls

# Get an instance of a logger
logger = logging.getLogger("apirest_rpì")


class PlayView(viewsets.ViewSet):
    """
    Starting to play the audio id X
    """
    serializer_class = MPDSerializer
    def update(self, request):
        serializer = MPDSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with connection():
                try:
                    client.playid(request.data['pos'])
                    status = "SUCCESS"
                    msg="Playing audio"
                except mpd.CommandError:
                    status="FAILURE"
                    msg="Command Error"

            response = apirest_response_format(request=request,
                                               status=status,
                                               msg=msg,
                                               result="",
                                               next_action='mpd/stop'
                                               )
            return Response(response)

class StopView(viewsets.ViewSet):
    """
    Stops playing
    """
    def update(self, request):
        with connection():
            try:
                client.stop()
                status = "SUCCESS"
                msg=""
            except mpd.CommandError:
                status="FAOLURE"
                msg="Command Error"

        response = apirest_response_format(request=request,
                                            status=status,
                                            msg=msg,
                                            result="",
                                           )
        return Response(response)


class MemoryView(viewsets.ViewSet):
    """
    Return statistics about system memory usage.
    More info: http://psutil.readthedocs.io/en/latest/#memory
    """

    def update(self, request):
        serializer = SoundSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            task = play_audio.delay(serializer.data['sound_path'])
            job = Job(
                name="play_audio",
                celery_id=task.id
            )
            job.save()
            # FIXME sync_job_db
            # play_audio.apply_async(serializer.data['sound_path'], job.id, link=sync_job_db.s())
            # (play_audio.s(serializer.data['sound_path'], job.id) | sync_job_db.s(job.id)).delay()

            msg_out = "Asyncronous task. play_audio: " + serializer.data['sound_path']
            response = apirest_response_format(request=request,
                                               status=task.status,
                                               msg=msg_out,
                                               result="",
                                               job_id=job.id,
                                               )
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
