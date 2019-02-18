# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

# Modelo abstrato de endereço.


class FullAddressModel(models.Model):
    address = models.CharField(_('logradouro'), max_length=255, null=True)
    number = models.CharField(_('número'), max_length=100, null=True)
    neighborhood = models.CharField(_('bairro'), max_length=100, null=True)
    city = models.CharField(_('cidade'), max_length=100)
    state = models.CharField(_('UF'), max_length=2)
    zipcode = models.CharField(_('CEP'), max_length=100, null=True)
    country = models.CharField(_('País'), max_length=100, null=True)
    # Point field para armazenamento de latitude e longitude com mais organização e simplicidade
    location = models.PointField(_('coordenadas'), null=True)

    class Meta:
        abstract = True
