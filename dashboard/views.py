from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger("dashboard")

# Create your views here.
@login_required(login_url="accounts/login")
def home(request):
    return render(request, "dashboard/home.html")


def context(type_device):
    preffix = type_device + "/env_sensor"
    print(preffix)
    context = {
        'type_device': type_device,
        'resource_temperature': preffix + "/temperature",
        'resource_humidity': preffix + "/humidity",
        'resource_pressure': preffix + "/pressure"
    }
    context['target_graphite_temperature'] = "localhost/" + context['resource_temperature']
    context['target_graphite_humidity'] = "localhost/" + context['resource_humidity']
    context['target_graphite_pressure'] = "localhost/" + context['resource_pressure']

    logger.debug(context)
    return context

@login_required(login_url="accounts/login")
def rpi(request, type_device):
    return render(request, 'dashboard/rpi.html', context(type_device))

@login_required(login_url="accounts/login")
def sensehat(request, type_device):
    return render(request, 'dashboard/env_sensor.html', context(type_device))

@login_required(login_url="accounts/login")
def sensehat_led_matrix(request, type_device):
    return render(request, 'dashboard/sensehat_led_matrix.html', context(type_device))

@login_required(login_url="accounts/login")
def dht(request, type_device):
    return render(request, 'dashboard/env_sensor.html', context(type_device))

