from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
# it will reject GET request
from django.views.decorators.csrf import csrf_exempt
# required since stripe do not send csfr token

from checkout.webhook_handler import StripeWH_Handler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """
    listen for webhooks from stripe
    code is available in the stripe documentation
    """
    # 1. setup the stripe api key
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # 2. get the webhook data and verify the signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
                                            payload,
                                            sig_header,
                                            wh_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # there are hundred different webhooks and it is not possible tohave
    # an if statement for each one. for this reason we will setup the handler

    # setup a webhook handler:
    # 1. create an instance passing the request
    handler = StripeWH_Handler(request)

    # 2. create a dictionary and map webhook events to relevant handler
    # functions the dictionary keys are the name of the webhooks coming from
    # stripe and the value is the actual methods inside the handlers
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_method_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # get the webhook event type from stripe and store it in a key called type
    event_type = event['type']

    # if there is an handler for it, get it from the event map
    # use the generic one by default event handler is an alias for any function
    # pulled out from dictionary above
    event_handler = event_map.get(event_type, handler.handle_event)

    # call the event handler with the event and return the response to stripe
    response = event_handler(event)
    return response
