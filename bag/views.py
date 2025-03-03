from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """a view that renders the shopping bag page"""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    add a quantity of the specified item in the shopping bag
    """
    # 1. get a quantity from the form and convert as integer
    quantity = int(request.POST.get('quantity'))
    # 2. get the redirect URL from the form used after the process is finished
    redirect_url = request.POST.get('redirect_url')
    # 3. store the information in a session (customer can continue to browse the site and it 
    # will save the information related to the shopping bag in the actual session)
    # this session persists until user close the browser
    # the variable bag will contain this information
    size = None

    # is the product has size, it will be set with this code:
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            # if an item is already in the bag, it will update the quantity if the size is the same:
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            # if the item already exist but with a different size, it will be added as is:
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # if items not in the bag, it will add it using the ID and the size as dictionary
            bag[item_id] = {'items_by_size':{size: quantity}}
    else:
        if item_id in list(bag.keys()):
            # if bag variable already exist in the session it will be updated
            bag[item_id] += quantity
        else: 
            # if the bag variable is not present in the session it will be created
            bag[item_id] = quantity

    # 4. overwrite the information in the session (python dictionary)
    request.session['bag'] = bag
    # 5. redirect the user back to the redirect url 
    return redirect(redirect_url)