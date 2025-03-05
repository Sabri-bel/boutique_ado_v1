from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver  # used for receive "signals"
from .models import OrderLineItem

@receiver(post_save, sender=OrderLineItem)
# the decorator make sure that the funxtion is executed anytime
# the post-save signal is sent
def update_on_save(sender, instance, created, **kwargs):
    """
    update the order total on lineitem update/create
    update total, delivery costs, and grand tital for each order as
    user add line items to it using a built-in features of 
    django called signals
    this function will handle signals from the post_save events
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
# the decorator make sure that the funxtion is executed anytime
# the post-save signal is sent
def delete_on_save(sender, instance, **kwargs):
    """
    update the order total on lineitem delete
    update total, delivery costs, and grand tital for each order as
    user add line items to it using a built-in features of 
    django called signals
    this function will handle signals from the post_save events
    """
    instance.order.update_total()