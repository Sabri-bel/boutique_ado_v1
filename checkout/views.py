from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
import stripe 

from .forms import OrderForm

from bag.contexts import bag_contents


# Create your views here.


def checkout(request):
    # this is the checkout view
    # 1. get the bag from the session
    bag = request.session.get('bag', {})
    if not bag:
        # error message if there is nothing in the bag
        messages.error(request, 'there is nothing in your bag at the moment')
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100) # stripes require an integer
 
    # 2. create an instance of the orderform
    order_form = OrderForm()
    # 3. create the template and the context
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51QzfVT2ZFWbLVbOJcbACwyVnLLefvIOPaP14A0O0BO54amj9NR0jdeO50LipAFx8O6GubWL3m3oYPAdfptkuagNR00602mtyom',
        'client_secret': 'test_client_secret',
    }
    return render(request, template, context)
