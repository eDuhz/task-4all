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

# ViewSet do modelo UserAddress
# Utiliza o serializador da classe (presente em serializers.py)
# Métodos possíveis GET e POST
# Paginação de 20 em 20 objetos.
# GETs unitários (api/address/users-address/{id}) e em lista (api/address/users-address/)
# Parâmetros de criação:
#  name (string), user (int), address (string), number (string),
#  neighborhood (string), city (string), state (string),
#  zipcode (string), longitude (float), latitude (float)
# Retornos de sucesso:
#  POST - HTTP_201_CREATED
#  GET - HTTP_200_OK


class UserAddressViewSet(ModelViewSet):

    permission_classes = (AllowAny,)
    serializer_class = UserAddressSerializer
    http_method_names = ['get', 'post']
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
                                   location=Point(request.data.get('longitude'), request.data.get('latitude'), srid=4326),
                                   country=request.data.get('country')
                                   )
        return Response({'success': 'Address created with success'}, status=HTTP_201_CREATED)


# ViewSet de arquivos de texto com pontos Geográficos
# Utiliza o serializador da classe (presente em serializers.py)
# Armazenei as files txt no banco de dados para possíveis backups e praticidade.
# Lê a file, extrai as informações e utiliza api do Nominatin (https://nominatim.openstreetmap.org/) para fazer o
# enriquecimento dos dados
# Retornos de sucesso:
#  POST - HTTP_201_CREATED
# Retornos de falha:
#  POST - HTTP_400_BAD_REQUEST


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

            # Limpa as strings retirando o \n do fim e pega apenas o valor de latitude e longitude
            for line in content:
                if 'Latitude' in line:
                    latitude.append(line.split('   ')[1].strip())
                if 'Longitude' in line:
                    longitude.append(line.split('   ')[1].strip())

            file.close()

            # Iteração sobre as listas com os dados de latitude e longitude
            for lat, lon in list(zip(latitude, longitude)):

                # Processo de enriquecimento dos dados
                location = geolocator.reverse(lat + ',' + lon)
                address = location.raw['address']

                # Há várias opções de retorno na api do Nominatim, porém é bem mais padronizada do que as possíveis.
                if {'house_number', 'road'} <= address.keys():
                    print('--- creating object type 1 ---\n')
                    UserAddress.objects.create(user=User.objects.get(pk=1), country=address['country'],
                                               name=address['road'] + ', ' + address['house_number'],
                                               address=address['road'], number=address['house_number'],
                                               neighborhood=address['suburb'], city=address['city'],
                                               state=address['state'], zipcode=address['postcode'],
                                               location=Point(float(lat), float(lon), srid=4326))
                elif 'road' in address:
                    print('--- creating object type 2 ---\n')
                    UserAddress.objects.create(user=User.objects.get(pk=1), country=address['country'],
                                               name=list(address.values())[0], address=address['road'],
                                               neighborhood=address['suburb'], city=address['city'],
                                               state=address['state'], zipcode=address['postcode'],
                                               location=Point(float(lat), float(lon), srid=4326))

                elif {'suburb', 'postcode'} <= address.keys():
                    print('--- creating object type 3 ---\n')
                    UserAddress.objects.create(user=User.objects.get(pk=1), country=address['country'],
                                               name=list(address.values())[0], address=list(address.values())[0],
                                               neighborhood=address['suburb'], city=address['city'],
                                               state=address['state'], zipcode=address['postcode'],
                                               location=Point(float(lat), float(lon), srid=4326))
                elif 'suburb' in address:
                    print('--- creating object type 4 ---\n')
                    UserAddress.objects.create(user=User.objects.get(pk=1), country=address['country'],
                                               name=list(address.values())[0], address=list(address.values())[0],
                                               neighborhood=address['suburb'], city=address['city'],
                                               state=address['state'],
                                               location=Point(float(lat), float(lon), srid=4326))

            return Response({'status': 'Geopoints added on DB and processed successfully'},
                            HTTP_201_CREATED)

        return Response({'status': 'Failed to process file'}, HTTP_400_BAD_REQUEST)


