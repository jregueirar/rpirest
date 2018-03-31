from apirest_dht import views
from django.conf.urls import url, include
from core.common import MyRouter

router = MyRouter()

# router.register(r'env_sensor/humidity', views.HumidityView, base_name='dht_humidity')
router.register(r'env_sensor/humidity', views.HumidityView, base_name='dht_humidity')
router.register(r'env_sensor/temperature', views.TemperatureView, base_name='dht_temperature')

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^', views.api_root, name='index_dht'),
    # url(r'^', views.APIRoot.as_view(), name='index_dht'),
    # url(r'^env_sensor/humidity', views.HumidityView.as_view(), name='dht_humidity'),
    # url(r'env_sensor/temperature', views.TemperatureView, name="dht_temperature")
]
