# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Job
from .common import MyRouter
from .common import apirest_response_format
from .serializers import DelaySerializer
from rest_framework import serializers
from rpirest.celery import sleep


def routes():
    router = MyRouter()
    router.register(r'job', TaskView, base_name='job')
    router.register(r'example_async_task', Sleep, base_name='task')
    return router.urls


class TaskView(viewsets.ViewSet):
    """
    Show the status of one Asyncronous Job.
    PK = Task Id.
    """
    def retrieve(self, request, pk=None):
        if pk is not None:
            response = apirest_response_format(request=request,
                                               status=None,
                                               msg=None,
                                               result=None,
                                               job_id=pk,
                                               )
            return Response(response)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

########
# Demo. Example of a Asyncronous Job: Sleep for X Seconds
########
class DelaySerializer(serializers.Serializer):
    time = serializers.IntegerField(default=10)

class Sleep(viewsets.ViewSet):
    """
    Example of a AsyncJob. Sleep for X seconds.
    """
    serializer_class = DelaySerializer

    def update(self, request):
        serializer = DelaySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            task = sleep.delay(serializer.data['time'])
            job = Job(
                name="sleep",
                celery_id=task.id
            )
            job.save()
            # FIXME sync_job_db

            msg_out="Async Job for testing. Sleep for X Seconds."
            response = apirest_response_format(request=request,
                                               status=task.status,
                                               msg=msg_out,
                                               result="",
                                               job_id=job.id,
                                               )
            return Response(response)
