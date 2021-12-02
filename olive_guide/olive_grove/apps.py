from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OliveGroveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'olive_grove'
    verbose_name = _("Olive Groves")
