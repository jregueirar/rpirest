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
    Starting to play the track in the position X. Position start at 1.
    """
    def list(self, request):
        with connection():
            try:
                playlist=client.playlist()
                result={}
                status = "SUCCESS"
                msg = "Listing the playlist. You need the id for playing"
            except mpd.CommandError:
                status = "FAILURE"
                msg = "Command Error"
        response = apirest_response_format(request=request, status=status, msg=msg, result=result)
        return Response(response)


    serializer_class = MPDSerializer
    def update(self, request):
        serializer = MPDSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with connection():
                try:
                    client.playid(request.data['position'])
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

