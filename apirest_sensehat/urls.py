from apirest_sensehat import views
from django.conf.urls import url, include
from core.common import MyRouter
import yaml


router = MyRouter()

router.register(r'env_sensor/humidity', views.HumidityView, base_name='humidity')
router.register(r'env_sensor/temperature', views.TemperatureView,
                base_name='temperature')
router.register(r'env_sensor/temperature_from_humidity', views.TemperatureFromHumidityView,
                base_name='temperature_from_humidity')
router.register(r'env_sensor/temperature_from_pressure', views.TemperatureFromPressureView,
                base_name='temperature_from pressure'),
router.register(r'env_sensor/pressure', views.PressureView,
                base_name='pressure')
router.register(r'led_matrix/rotation', views.RotationView,
                base_name='rotation')
router.register(r'led_matrix/flip_h', views.FlipHView,
                base_name='flip_h')
router.register(r'led_matrix/flip_v', views.FlipVView,
                base_name='flip_v')
router.register(r'led_matrix/pixels', views.PixelsView,
                base_name='pixels')
router.register(r'led_matrix/load_image', views.LoadImageView,
                base_name='load_image')
router.register(r'led_matrix/clear', views.ClearView,
                base_name='clear')
router.register(r'led_matrix/show_message', views.ShowMessageView,
                base_name='show_message')
router.register(r'led_matrix/show_letter', views.ShowLetterView,
                base_name='show_letter')
router.register(r'led_matrix/low_light', views.LowLightView,
                base_name='low_light')
router.register(r'led_matrix/gamma', views.GammaView,
                base_name='gamma')
router.register(r'imu_sensor/imu_config', views.ImuConfigView,
                base_name='imu_config')
router.register(r'imu_sensor/orientation_radians', views.OrientationRadiansView,
                base_name='orientation_radians')
router.register(r'imu_sensor/orientation_degrees', views.OrientationDegreesView,
                base_name='orientation_degrees')
router.register(r'imu_sensor/orientation', views.OrientationDegreesView,
                base_name='orientation')
router.register(r'imu_sensor/compass', views.CompassView,
                base_name='compass')
router.register(r'imu_sensor/compass_raw', views.CompassRawView,
                base_name='compass_raw')
router.register(r'imu_sensor/gyroscope', views.GyroscopeView,
                base_name='gyroscope')
router.register(r'imu_sensor/gyroscope_raw', views.GyroscopeRawView,
                base_name='gyroscope_raw')
router.register(r'imu_sensor/accelerometer', views.AccelerometerView,
                base_name='accelerometer')
router.register(r'imu_sensor/accelerometer_raw', views.AccelerometerRawView,
                base_name='accelerometer_raw')

urlpatterns = [
    url(r'^', include(router.urls)),
]
