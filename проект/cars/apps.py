from django.apps import AppConfig


class CarsConfig(AppConfig):
    """Конфигурация Django-приложения cars."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "cars"
