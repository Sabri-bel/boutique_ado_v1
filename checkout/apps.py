from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        # override the ready method and importing the
        # signals module
        # everytime a line item is saved or deleted, the custom
        # update model is called
        import checkout.signals
