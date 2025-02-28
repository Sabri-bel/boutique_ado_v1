from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """ 
    
    """

    bag_items = []
    total = 0
    product_count = 0
    # below how to render the page:get the session if already or initialize a new one
    bag = request.session.get('bag', {})

    # iterate through all the items in the shopping bag:
    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            # if item_data has no size (so it is an integer and not a dictionary):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            # below append information in the empty list created above
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                })
        else:
            # if the item_data has quantity+size it is a dictionary:
            product = get_object_or_404(product, pk=item_id)
            
            # we need to iterate through the inner dictionary items_by_size
            for size, quantity in item_data['items_by_size'].items():
                # increment the product count and total accordingly
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                'size': size
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
