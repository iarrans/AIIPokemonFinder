from django.apps import AppConfig
import django.db.models.fields

class MainConfig(AppConfig):
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    name = 'main'
