from rest_framework.response import Response
from rest_framework import viewsets, status
from apirest.serializers import *
from rest_framework.decorators import detail_route, list_route
from sense_hat import SenseHat
from rest_framework.views import APIView
from rest_framework.reverse import reverse

sense = SenseHat()


class APIRoot(APIView):

    def get(self, request):
        # Assuming we have views named 'foo-view' and 'bar-view'
        # in our project's URLconf.
        return Response({
            'foo': reverse('PixelView', request=request)
        })


#@list_route(methods=['post', 'delete'])
#Prueba.
class HumidityView(viewsets.ViewSet):
    """
    Gets the current temperature in degrees Celsius from the humidity sensor.
    """
    def list(self, request):
        result = sense.get_humidity()
        return Response({'Result': result})


class TemperatureView(viewsets.ViewSet):
    """
    Gets the current temperature in degrees Celsius from the humidity sensor.
    Api rest of get_temperature_from_humidity.
    [ref]: https://pythonhosted.org/sense-hat/api/#environmental-sensors
    """

    def listView(self, request):
        result = sense.get_temperature_from_humidity()
        return Response({'Result': result})



class TemperatureFromHumidityView(viewsets.ViewSet):
    """
    https://pythonhosted.org/sense-hat/api/#environmental-sensors
    Gets the current temperature in degrees Celsius from the humidity sensor.
    """

    def list(self, request):
        result = sense.get_temperature_from_humidity()
        return Response({'Result': result})


class TemperatureFromPressureView(viewsets.ViewSet):
    """
    Gets the current temperature in degrees Celsius from the humidity sensor.
    """

    def list(self, request):
        result = sense.get_temperature_from_pressure()
        return Response({'Result': result})


class PressureView(viewsets.ViewSet):
    """
    https://pythonhosted.org/sense-hat/api/#environmental-sensors
    Gets the current temperature in degrees Celsius from the humidity sensor.
    """

    def list(self, request):
        result = sense.get_pressure()
        return Response({'Result': result})


class PixelView(viewsets.ViewSet):
    """
        PixelView
    """
    serializer_class = PixelSerializer
    lookup_value_regex = '[0-7],[0-7]'

    def list(self, request):
        print("List")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = PixelSerializer(data=request.data)
        if serializer.is_valid():
            sense.set_pixel(serializer.data['x'],
                            serializer.data['y'],
                            serializer.data['r'],
                            serializer.data['g'],
                            serializer.data['b'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        print ("Retrieve")
        if pk is not None:
            x, y = pk.split(sep=",")
            serializer = XYSerializer(data={'x': int(x), 'y': int(y)})
            if serializer.is_valid():
                data = serializer.data
                color = sense.get_pixel(data['x'], data['y'])
                serializer_response = {'x':data['x'], 'y': data['y'],
                                       'r': color[0], 'g': color[1],
                                       'b': color[2]}
            return Response(serializer_response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # FIXME: No funciona
    def metadata(self, request):
        """
        Don't include the view description in OPTIONS responses.
        """
        data = super(PixelView, self).metadata(request)
        data.pop('description')
        # data.add({"tutua":'probando'})
        return data


class PixelsView(viewsets.ViewSet):
    lookup_value_regex = '[0-7],[0-7]'
    serializer_class = PixelSerializer


    def get_queryset(self):
        pixel_list = sense.get_pixels()
        queryset_list = []

        i = 0
        for pixel_color in pixel_list:
            coordinates = Pixel.get_coordinates(i)

            queryset_list.append(Pixel(x=coordinates['x'], y=coordinates['y'],
                                       r=pixel_color[0],
                                       g=pixel_color[1],
                                       b=pixel_color[2]))
            i += 1

        return queryset_list

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PixelSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        x, y = pk.split(sep=",")
        serializer = XYSerializer(data={'x': int(x), 'y': int(y)})
        if serializer.is_valid():
            data = serializer.data
            color = sense.get_pixel(data['x'], data['y'])
            serializer_response = {'x':data['x'], 'y': data['y'],
                                   'r': color[0], 'g': color[1],
                                   'b': color[2]}
            return Response(serializer_response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = MatrixSerializer(data=request.data)
        if serializer.is_valid():
            sense.set_pixels(serializer.data['x'],
                            serializer.data['y'],
                            serializer.data['r'],
                            serializer.data['g'],
                            serializer.data['b'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request):
    #     serializer = PixelSerializer(data=request.data)
    #     if serializer.is_valid():
    #         data = serializer.data
    #         sense.set_pixel(data['x'], data['y'], data['r'], data['g'], data['b'])
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @list_route()
    @detail_route(methods=['post'])
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


from rest_framework import authentication, permissions
from rest_framework.views import APIView

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)