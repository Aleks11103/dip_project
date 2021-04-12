from django.shortcuts import render
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart
from home.models import Category, Subcategory
from django.template.defaulttags import register


@register.filter
def dict_key(dictionary, key):
    return dictionary[key]

def order_create(request):
    cart = Cart(request)
    categories = Category.objects.all()
    subcategories = {}
    if categories:
        for category in categories:
            subcategories[category] = Subcategory.objects.filter(category_id=category)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(
                request,
                'orders/created.html',
                {
                    'order': order,
                    'categories': categories,
                    'subcategories': subcategories,
                }
            )
    else:
        form = OrderCreateForm
    return render(
        request,
        'orders/create.html',
        {
            'cart': cart,
            'form': form,
            'categories': categories,
            'subcategories': subcategories,
        }
    )