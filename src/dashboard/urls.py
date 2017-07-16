from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^overview$', TemplateView.as_view(template_name="dashboard/home.html"), name='home'),
    url(r'^control-led-matrix$', TemplateView.as_view(template_name="dashboard/control_led_matrix.html"), name='led_matrix'),
    url(r'^env-sensors$', TemplateView.as_view(template_name="dashboard/env_sensors.html"), name='led_matrix'),
    url(r'^example-jquery$', TemplateView.as_view(template_name="example-sensehatjs.html"), name='example_jquery'),
    url(r'^base$', TemplateView.as_view(template_name="dashboard/ull_base.html"), name='base'),
    url(r'^base2$', TemplateView.as_view(template_name="base_example.html"), name='base'),
]
