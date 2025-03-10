from django.shortcuts import render, redirect, reverse  # type: ignore
from django.contrib import messages  # type: ignore
from django.conf import settings  # type: ignore
import stripe  # type: ignore

from .forms import OrderForm

from bag.contexts import bag_contents


# Create your views here.


def checkout(request):
    # this is the checkout view

    # stipe payment related variables:
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # 1. get the bag from the session
    bag = request.session.get('bag', {})
    if not bag:
        # error message if there is nothing in the bag
        messages.error(request, 'there is nothing in your bag at the moment')
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']

    stripe_total = round(total * 100)  # stripes require an integer

    stripe.api_key = stripe_secret_key

    # create the payment intent giving the amount and the currency:
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # 2. create an instance of the orderform
    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing, \
        did you forget to set it in your environment?')

    # 3. create the template and the context
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)
