from apirest_dht import views
from django.conf.urls import url, include
from core.common import MyRouter

router = MyRouter()

router.register(r'env_sensor/humidity', views.HumidityView, base_name='dht_humidity')
router.register(r'env_sensor/temperature', views.TemperatureView, base_name='dht_temperature')

urlpatterns = [
    url(r'^', include(router.urls)),
]
