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
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'env_sensors/humidity', views.HumidityView, base_name='humidity')
router.register(r'env_sensors/temperature', views.TemperatureView,
                base_name='temperature')
router.register(r'env_sensors/temperature_from_humidity', views.TemperatureFromHumidityView,
                base_name='temperature_from_humidity')
router.register(r'env_sensors/temperature_from_pressure', views.TemperatureFromPressureView,
                base_name='temperature_from pressure'),
router.register(r'env_sensors/pressure', views.PressureView,
                base_name='pressure')
router.register(r'led_matrix/pixels', views.PixelsView,
                base_name='pixels')
router.register(r'led_matrix/pixel', views.PixelView, base_name='pixel')

urlpatterns = [
    url(r'^', include(router.urls)),
]


#PixelViewSet = views.PixelViewSet.as_view({'get': 'retrieve'})
# urlpatterns = [
#       url(r'^$', views.APIRoot.as_view()),
#       url(r'^led_matrix/pixel', views.PixelView.as_view(), name='pixel'),
      # url(r'^led_matrix/pixel/(<x>[0-7],<y>[0-7])$', views.PixelView.as_view),
 # ]
