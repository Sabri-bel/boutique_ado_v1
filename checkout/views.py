from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

# Create your views here.


def checkout(request):
    # this is the checkout view
    # 1. get the bag from the session
    bag = request.session.get('bag', {})
    if not bag:
        # error message if there is nothing in the bag
        messages.error(request, 'there is nothing in your bag at the moment')
        return redirect(reverse('products'))

    # 2. create an instance of the orderform
    order_form = OrderForm()
    # 3. create the template and the context
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
    }
    return render(request, template, context)
