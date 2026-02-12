from django.apps import AppConfig


class TattooShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tattoo_shop'

    def ready(self):
        import tattoo_shop.signals
