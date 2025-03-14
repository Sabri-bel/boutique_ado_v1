from django.shortcuts import render, redirect, reverse, get_object_or_404  # type: ignore
from django.contrib import messages  # type: ignore
from django.conf import settings  # type: ignore
import stripe  # type: ignore

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents


# Create your views here.


def checkout(request):
    # this is the checkout view

    # stipe payment related variables:
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        # create an instance of the form
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        # if the form is valid we can save the form and iterate each item
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    # 1. we get the item_id of the product
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
                except Product.DoesNotExist:
                    # 2. handle an error if the product is not existing:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in database."
                        "Please call us for assistance!")
                    )
                    # delete the order and come back at the shopping bag page
                    order.delete()
                    return redirect(reverse('view_bag'))

            # if the customer decided to save their profile info or not:
            request.session['save_info'] = 'save-info' in request.POST

            # finally, redirect the customer to a new page
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            # if the order form is not valid:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
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


def checkout_success(request, order_number):
    """
    handle successful checkout, it will take the order number and
    render a nice successful page with payment confirmation
    """
    # 1. check if the user want to save information
    save_info = request.session.get('save_info')

    # 2. get the order created using the order number
    order = get_object_or_404(Order, order_number=order_number)

    # 3. display a success message with the relevant information
    messages.success(request, f"Order succesfully processed! \
                     Your order number is {order_number} \
                     a confirmation will be sent to {order.email}.")

    # 4. delete the shopping bag no longer needed
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
