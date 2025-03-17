from django.http import HttpResponse  # type: ignore


class StripeWH_handler:
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
        return HttpResponse(
            content=f"Webhook received: {event['type']}",
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        handle a failure intent webhook event
        it will take the event of stripe and return an http response
        """
        return HttpResponse(
            content=f"Webhook received: {event['type']}",
            status=200)
