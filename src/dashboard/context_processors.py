from django.conf import settings
from apirest.models import AttachedDevices


def global_settings(request):
    # return any necessary values
    list=[]
    for i in AttachedDevices.objects.all():
        list.append(i.type)

    return {
        'GRAPHITE_URL': settings.GRAPHITE_URL,
        'API_REST_URL': settings.API_REST_URL,
        'GRAFANA_URL': settings.GRAFANA_URL,
        'DEVICES_ATTACHED': list,
        'attached_devices_list': AttachedDevices.objects.all()
    }
