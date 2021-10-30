from django.contrib.gis.db import models
from django.contrib.gis.measure import Area
from django.contrib.auth.models import User
from utils.weather import getWeather
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

User._meta.get_field('email')._unique = True

class OliveGrove(models.Model):
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateField(_("Created At"), auto_now_add=True)
    name=models.CharField(_("Name"), max_length=50)
    polygon=models.PolygonField(_("Polygon"))
    GREEK=2100
    GLOBAL=4326
    SRID_CHOICES = [
        (GREEK, _('Greek')),
        (GLOBAL, _('Global')),
    ]
    srid=models.IntegerField(_('Coordinate System'), choices=SRID_CHOICES,default=4326)

    class Meta:
        verbose_name = _("Olive Grove")
        verbose_name_plural = _("Olive Groves")
    @property
    def weather(self):
        return getWeather(self.polygon)
    @property
    def acres(self):
        poly=self.polygon.clone()
        if self.srid==2100:
            poly.transform(2100)
            return poly.area/1000
        else:
            return poly.area
    @property
    def coordinates(self):
        poly=self.polygon.clone()
        if self.srid==2100:
            poly.transform(2100)
        return poly.coords

    def get_absolute_url(self):
        return reverse('olive_grove:olive_grove_detail', kwargs={'pk': self.pk})
    def __str__(self):
        return self.name
class Note(models.Model):
    created_by=models.ForeignKey(User,on_delete=models.CASCADE )
    olive_grove=models.ForeignKey(OliveGrove,on_delete=models.CASCADE )
    created_at=models.DateField(_("Created At"), auto_now_add=True)
    title=models.CharField(_("Title"), max_length=50)
    text=models.TextField(_("Text"))
    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
    def get_absolute_url(self):
        return reverse('olive_grove:note_detail', kwargs={'og_id':self.olive_grove.pk,'pk': self.pk})
    def __str__(self):
        return self.title
