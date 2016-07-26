from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="env_sensors.html"), name='dashboard'),
    url(r'^json_examples$', TemplateView.as_view(template_name="json_examples.html"), name='example'),
    url(r'^led_matrix$', TemplateView.as_view(template_name="led_matrix.html"), name='led_matrix'),
    url(r'^example_jquery$', TemplateView.as_view(template_name="example-sensehatjs.html"), name='example_jquery'),
]
