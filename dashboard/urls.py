from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^overview$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^control_led_matrix$', TemplateView.as_view(template_name="control_led_matrix.html"), name='led_matrix'),
    url(r'^example_jquery$', TemplateView.as_view(template_name="example-sensehatjs.html"), name='example_jquery'),
    url(r'^base$', TemplateView.as_view(template_name="ull_base.html"), name='base'),
    url(r'^base2$', TemplateView.as_view(template_name="analitic_base.html"), name='base'),
]
