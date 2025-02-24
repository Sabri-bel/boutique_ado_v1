from django.contrib import admin
from .models import Product, Category

# Register your models here.


class productAdmin(admin.ModelAdmin):
    # show the fields available in the admin pane
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    ordering = ('sku',)


class categoryAdmin(admin.ModelAdmin):
    # show the fields available in the admin pane
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, productAdmin)
admin.site.register(Category, categoryAdmin)
