# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class FullAddressModel(models.Model):
    address = models.CharField(_('logradouro'), max_length=255, null=True)
    number = models.CharField(_('número'), max_length=100, null=True)
    address2 = models.CharField(
        _('complemento'), max_length=100, blank=True, null=True
    )
    neighborhood = models.CharField(_('bairro'), max_length=100, null=True)

    city = models.CharField(_('cidade'), max_length=100)
    state = models.CharField(_('UF'), max_length=2)
    zipcode = models.CharField(_('CEP'), max_length=100, null=True)

    location = models.PointField(_('coordenadas'), null=True)

    class Meta:
        abstract = True
