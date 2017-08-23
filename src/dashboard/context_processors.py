from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'GRAPHITE_URL': settings.GRAPHITE_URL,
        'API_REST_URL': settings.API_REST_URL,
        'GRAFANA_URL': settings.GRAFANA_URL
    }
