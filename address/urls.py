from django.conf.urls import url, include
from rest_framework import routers
from .viewsets import UserAddressViewSet, GeoPointsTextViewSet

router = routers.DefaultRouter()
router.register(r'users-address', viewset=UserAddressViewSet, base_name='UserAddress')
router.register(r'geo-points', viewset=GeoPointsTextViewSet, base_name='GeoPoints')
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
]