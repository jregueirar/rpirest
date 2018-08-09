from rest_framework import routers
from rest_framework.routers import Route, DynamicDetailRoute, DynamicListRoute
from .models import Job
from celery.result import AsyncResult

# Custom Route for change suffix and mapping
class MyRouter(routers.DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'put': 'update',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': ''}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicListRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update_element',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Value'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]

# Syncing info of Job with AsyncResult
#def sync_job_db(job_id):

#    job = Job.objects.get(pk=job_id)
#    res = AsyncResult(job.celery_id)
#    res.result
#    #job.completed = res._cache['date_done']
#    job.status = res.status
#    job.save()


def apirest_response_format(request, status, msg, result, job_id=None):
    response={'url': request.build_absolute_uri()}
    response['status'] = status
    response['msg'] = msg
    response['result'] = result

    # Used in asynchronous tasks
    if job_id:
        job = Job.objects.get(pk=job_id)
        response['asyncronous_task'] = {}
        response['asyncronous_task']['jobid'] = job.id
        response['asyncronous_task']['name'] = job.name
        response['asyncronous_task']['celery_id'] = job.celery_id
        check_job_url = request.build_absolute_uri('/')[:-1].strip("/") + "/api/v1/core/job/" + str(job_id)
        response['asyncronous_task']['check_job_url'] = check_job_url
        response['asyncronous_task']['created'] = job.created

        res = AsyncResult(job.celery_id)
        response['asyncronous_task']['status'] = res.state
        if res.state == 'FAILURE' or res.state == 'SUCCESS':
            res.result
            response['asyncronous_task']['completed'] = res._cache['date_done']

    return response
