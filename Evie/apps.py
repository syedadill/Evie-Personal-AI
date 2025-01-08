from django.apps import AppConfig


class EvieConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Evie'


def ready(self):
    import Evie.signals

    