from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'GRAPHITE_LOCAL_URL': settings.GRAPHITE_LOCAL_URL,
        'API_REST_URL': settings.API_REST_URL
    }
