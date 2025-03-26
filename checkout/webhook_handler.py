from django.http import HttpResponse  # type: ignore
import stripe  # type:ignore

from .models import Order, OrderLineItem
from products.models import Product

import json
import time


class StripeWH_Handler:
    """
    handle stripe webhook
    this is a notification for each operation of stripe (such as payment
    intent being created, payment complete and so on)
    webhooks are like signals django send every time a model is saved or
    deleted, but they are sent using a secure URL provided
    """
    def __init__(self, request):
        # init is called everytime an instance is created
        # we are going to use it to assign the request as an attribute
        # of the class
        self.request = request

    def handle_event(self, event):
        """
        handle a generic/unknown/unexpected webhook event
        it will take the event of stripe and return an http response
        """
        return HttpResponse(
            content=f"unhandled Webhook received: {event['type']}",
            status=200)

    def handle_payment_method_succeeded(self, event):
        """
        handle payment intent success webhook event
        it will take the event of stripe and return an http response
        """
        # get the payment intent:
        intent = event.data.object

        # 2. use the intent above to create an order (if the user close the
        # browser or refresh the page on loading)
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # get the charge object
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)

        # store the billing details, shipping and grandtotal
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # clean the data in the shipping details - replace empty with none
        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None
        
        # if the order doesnt exist:
        order_exists = False
        # create a delay for aviod multiple creation based on delayed response:
        attempt = 1
        while attempt < 5:
            try:
                # get the order using the information from payment intent
                order = Order.object.get(
                    # use the __iexact for get the exact match but not case sensitive
                    full_name__iexact=shipping_details.name,
                    email__iexact=shipping_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.country,
                    postcode__iexact=shipping_details.postal_code,
                    town_or_city__iexact=shipping_details.city,
                    street_address1__iexact=shipping_details.line1,
                    street_address2__iexact=shipping_details.line2,
                    county__iexact=shipping_details.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # if the order exists:
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                    content=f"Webhook received: {event['type']} | SUCCESS: Verified order already in database", 
                    status=200)
        else:
            order = None

            # if the order does not exist, we will create like if the form were submitted
            try:
                order = Order.objects.create(
                # use the data from the payment intent
                        full_name=shipping_details.name,
                        email=shipping_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.country,
                        postcode=shipping_details.postal_code,
                        town_or_city=shipping_details.city,
                        street_address1=shipping_details.line1,
                        street_address2=shipping_details.line2,
                        county=shipping_details.state,
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                )
                # 1. we get the item_id of the product
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        # if the product is an integer means no size
                        order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,  # no size
                        )
                        # save
                        order_line_item.save()
                    else:
                        # for product with sizes (dictionary) iterate each
                        # size and create a line accordingly:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    product_size=size,
                                )
                            # save
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
            return HttpResponse(
                content=f"Webhook received: {event['type']} | SUCCESS: created order in webhook",
                status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        handle a failure intent webhook event
        it will take the event of stripe and return an http response
        """
        return HttpResponse(
            content=f"Webhook received: {event['type']}",
            status=200)
