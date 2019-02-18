from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .viewsets import UserAddressViewSet
from django.contrib.auth.models import User


# Testes unitários para a API de endereços


class UserAddressAPITests(APITestCase):

    # Inicializa o banco de dados com um usuário dummy e as variáveis para teste.
    def setUp(self):
        User.objects.create_user(username='1', email='teste@teste.com', password='senhateste')
        self.user = 1
        self.name = 'Casa Unit Test'
        self.address = "Rua Erechim"
        self.number = '1170'
        self.neighborhood = 'Nonoai'
        self.city = 'Porto Alegre'
        self.state = 'RS'
        self.zipcode = '90830-000'
        self.latitude = -30.09224797
        self.longitude = -51.21528983
        self.country = 'Brasil'
        self.viewset = UserAddressViewSet.as_view(actions={'post': 'create', 'get': 'list'})

    # Teste de criação de objeto UserAddress
    def test_create_object(self):
        factory = APIRequestFactory()
        request = factory.post(path='/api/address/users-address/',
                               data={
                                   'user': self.user, 'name': self.name, 'country': self.country,
                                   'address': self.address, 'number': self.number,
                                   'neighborhood': self.neighborhood, 'city': self.city,
                                   'state': self.state, 'zipcode': self.zipcode,
                                   'latitude': self.latitude, 'longitude': self.longitude
                               }, format='json')

        response = self.viewset(request)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    # Teste do get da url da lista de objetos UserAddress
    def test_get_object(self):
        factory = APIRequestFactory()
        request = factory.get(path='/api/address/users-address/')

        response = self.viewset(request)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    # Teste do get da url de objeto UserAddress
    def test_get_single_object(self):
        factory = APIRequestFactory()
        request = factory.get(path='/api/address/users-address/1')

        response = self.viewset(request)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
