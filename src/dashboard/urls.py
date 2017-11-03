from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^rpi$', views.rpi, {'type_device': 'rpi'}),
    url(r'^sensehat$', views.sensehat, {'type_device': 'sensehat'}),
    url(r'^sensehat/led_matrix$', views.sensehat_led_matrix, {'type_device': 'sensehat'}),
    url(r'^dht11$', views.dht, {'type_device': 'dht11'}),
    url(r'^dht22$', views.dht, {'type_device': 'dht22'}),
    url(r'^am2302$', views.dht, {'type_device': 'am2302'}),
    url(r'^env-sensors$', TemplateView.as_view(template_name="dashboard/env_sensors.html"), name='led_matrix'),
    url(r'^example_jquery$', TemplateView.as_view(template_name="example-sensehatjs.html"), name='example_jquery'),
    url(r'^base$', TemplateView.as_view(template_name="dashboard/ull_base.html"), name='base'),
    url(r'^base2$', TemplateView.as_view(template_name="base_example.html"), name='base'),
]
