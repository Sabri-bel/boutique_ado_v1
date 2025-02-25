from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q  # generate a search query since filter method
# requires the searched part in both description and name. q can be used for search only in the name OR description
from .models import Product

# Create your views here.


def all_products(request):
    """a view to shows all products page"""
    products = Product.objects.all()
    query = None
    # below the code is used for filtering the product based on a search query
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "you didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """a view to show individual product details"""
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)
