from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.


class OrderLineItemAdminInline(admin.TabularInline):
    # allow us to add and edit line items in the admin from the
    # inside of the order model
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    # readonly fields are automatically calculated by the models
    # they cannot be manipulated by anyone
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag', 'stripe_pid',)

    # fields will allow us to specify the order of the fields in the
    # admin interface (otherwise it will be automatically adjusted
    # due to the read only fields)
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag', 'stripe_pid',)

    # list display will restrict the columns that show up in the
    # order list to only few key items
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    # set the order in reverse chronological - most recent first
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
