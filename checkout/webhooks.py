from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
# it will reject GET request
from django.views.decorators.csrf import csrf_exempt
# required since stripe do not send csfr token

from checkout.webhook_handler import StripeWH_handler

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

    print('success')
    return HttpResponse(status=200)