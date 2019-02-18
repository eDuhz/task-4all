from django.db import models
from base.models import FullAddressModel
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class UserAddress(FullAddressModel):
    user = models.ForeignKey(User, verbose_name=_('usuário'), on_delete=models.CASCADE)
    name = models.CharField(_('nome'), max_length=100)

    class Meta:
        verbose_name = _('endereço')
        verbose_name_plural = _('endereços')

    def __str__(self):
        return '{} - {}'.format(self.user, self.zipcode)

    def to_dict(self):
        return {
            'state': self.state,
            'city': self.city,
            'address': self.address,
            'number': self.number,
            'neighborhood': self.neighborhood,
            'zipcode': self.zipcode,
            'address2': self.address2,
            'location': {
                'lng': self.location.x,
                'lat': self.location.y
            }
        }


#Model that keep record from every geopoint added

class GeoPointsText(models.Model):
    text_file = models.FileField()

    class Meta:
        verbose_name = _('Ponto geométrico')
        verbose_name_plural = _('Pontos geométricos')

    def path(self):
        return self.text_file.path

