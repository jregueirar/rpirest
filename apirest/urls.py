from apirest import views
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.routers import Route, DynamicDetailRoute, DynamicListRoute


# Custom Route for change suffix and mapping
class MyRouter(routers.DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'put': 'update',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': ''}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicListRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update_element',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Value'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]


router = MyRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
router.register(r'env_sensors/humidity', views.HumidityView, base_name='humidity')
router.register(r'env_sensors/temperature', views.TemperatureView,
                base_name='temperature')
router.register(r'env_sensors/temperature_from_humidity', views.TemperatureFromHumidityView,
                base_name='temperature_from_humidity')
router.register(r'env_sensors/temperature_from_pressure', views.TemperatureFromPressureView,
                base_name='temperature_from pressure'),
router.register(r'env_sensors/pressure', views.PressureView,
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


#PixelViewSet = views.PixelViewSet.as_view({'get': 'retrieve'})
# urlpatterns = [
#       url(r'^$', views.APIRoot.as_view()),
#       url(r'^led_matrix/pixel', views.PixelView.as_view(), name='pixel'),
      # url(r'^led_matrix/pixel/(<x>[0-7],<y>[0-7])$', views.PixelView.as_view),
 # ]
