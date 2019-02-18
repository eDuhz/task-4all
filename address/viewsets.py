from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import AllowAny
from .serializers import UserAddressSerializer, GeoPointsTextSerializer
from .models import UserAddress, GeoPointsText
from geopy.geocoders import Nominatim


class UserAddressViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserAddressSerializer
    http_method_names = ['get']
    pagination_class = None
    queryset = UserAddress.objects.all()


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

            location = geolocator.reverse(latitude[9] + ',' + longitude[9])
            address = location.raw

            # for lat, lon in list(zip(latitude, longitude)):
            #
            #     location = geolocator.reverse(lat + ',' + lon)
            #     address = location.raw
            #
            # if 'city' in address:
            #     if {'house_number', 'road'} <= address.keys():
            #         UserAddress.objects.create(user=User.objects.get(pk=1),
            #                                    name=address['road'] + ', ' + address['house_number'],
            #                                    address=address['road'], number=address['house_number'],
            #                                    neighborhood=address['suburb'], city=address['city'],
            #                                    state=address['state'], zipcode=address['postcode'],
            #                                    location=Point(float(lat), float(lon), srid=4326))
            #     elif 'road' in address:
            #         UserAddress.objects.create(user=User.objects.get(pk=1),
            #                                    name=address['road'], address=address['road'],
            #                                    neighborhood=address['suburb'], city=address['city'],
            #                                    state=address['state'], zipcode=address['postcode'],
            #                                    location=Point(float(lat), float(lon), srid=4326))
            #
            #     elif {'suburb', 'postcode'} <= address.keys():
            #         UserAddress.objects.create(user=User.objects.get(pk=1),
            #                                    name=list(address.values())[9], address=list(address.values())[9],
            #                                    neighborhood=address['suburb'], city=address['city'],
            #                                    state=address['state'], zipcode=address['postcode'],
            #                                    location=Point(float(lat), float(lon), srid=4326))
            # else:
            #     if 'state' in address:
            #         UserAddress.objects.create(user=User.objects.get(pk=1), name=address['county'],
            #                                    address=address['county'], state=address['state'],
            #                                    location=Point(float(lat), float(lon), srid=4326))

            file.close()
            return Response({'status': 'Geopoints added on DB and processed successfully', 'geo': address},
                            HTTP_201_CREATED)

        return Response({'status': 'Failed to process file'}, HTTP_400_BAD_REQUEST)


