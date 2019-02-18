from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import AllowAny
from .serializers import UserAddressSerializer, GeoPointsTextSerializer
from .models import UserAddress, GeoPointsText
from geopy.geocoders import Nominatim


class UserAddressViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserAddressSerializer
    http_method_names = ['get', 'post']
    pagination_class = None
    queryset = UserAddress.objects.all()

    def create(self, request, *args, **kwargs):
        UserAddress.objects.create(name=request.data.get('name'),
                                   user=User.objects.get(pk=request.data.get('user')),
                                   address=request.data.get('address'),
                                   number=request.data.get('number'),
                                   neighborhood=request.data.get('neighborhood'),
                                   city=request.data.get('city'),
                                   state=request.data.get('state'),
                                   zipcode=request.data.get('zipcode'),
                                   location=Point(request.data.get('longitude'), request.data.get('latitude'), srid=4326)
                                   )
        return Response({'success': 'Address created with success'}, status=HTTP_201_CREATED)


class GeoPointsTextViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = GeoPointsTextSerializer
    http_method_names = ['post']
    pagination_class = None
    queryset = GeoPointsText.objects.all()

    def create(self, request, *args, **kwargs):
        _file = request.data.get('text_file', None)

        if _file:

            geolocator = Nominatim(user_agent='admissiontask')
            f = GeoPointsText.objects.create(text_file=_file)
            file = open(f.path())
            content = file.readlines()
            latitude = []
            longitude = []

            for line in content:
                if 'Latitude' in line:
                    latitude.append(line.split('   ')[1].strip())
                if 'Longitude' in line:
                    longitude.append(line.split('   ')[1].strip())

            for lat, lon in list(zip(latitude, longitude)):

                location = geolocator.reverse(lat + ',' + lon)
                address = location.raw['address']
                print(address)

                if {'house_number', 'road'} <= address.keys():
                    print('--- creating object type 1 ---\n')
                    UserAddress.objects.create(user=User.objects.get(pk=1),
                                               name=address['road'] + ', ' + address['house_number'],
                                               address=address['road'], number=address['house_number'],
                                               neighborhood=address['suburb'], city=address['city'],
                                               state=address['state'], zipcode=address['postcode'],
                                               location=Point(float(lat), float(lon), srid=4326))
                elif 'road' in address:
                    print('--- creating object type 2 ---\n')
                    UserAddress.objects.create(user=User.objects.get(pk=1),
                                               name=list(address.values())[0], address=address['road'],
                                               neighborhood=address['suburb'], city=address['city'],
                                               state=address['state'], zipcode=address['postcode'],
                                               location=Point(float(lat), float(lon), srid=4326))

                elif {'suburb', 'postcode'} <= address.keys():
                    print('--- creating object type 3 ---\n')
                    UserAddress.objects.create(user=User.objects.get(pk=1),
                                               name=list(address.values())[0], address=list(address.values())[0],
                                               neighborhood=address['suburb'], city=address['city'],
                                               state=address['state'], zipcode=address['postcode'],
                                               location=Point(float(lat), float(lon), srid=4326))
                elif 'suburb' in address:
                    print('--- creating object type 4 ---\n')
                    UserAddress.objects.create(user=User.objects.get(pk=1),
                                               name=list(address.values())[0], address=list(address.values())[0],
                                               neighborhood=address['suburb'], city=address['city'],
                                               state=address['state'],
                                               location=Point(float(lat), float(lon), srid=4326))

            file.close()
            return Response({'status': 'Geopoints added on DB and processed successfully'},
                            HTTP_201_CREATED)

        return Response({'status': 'Failed to process file'}, HTTP_400_BAD_REQUEST)


