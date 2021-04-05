from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from home.models import Product, Category, Subcategory
from cart.cart import Cart
from django.conf import settings
from cart.forms import CartAddProductForm
from django.template.defaulttags import register


@register.filter
def dict_key(dictionary, key):
    return dictionary[key]

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    subcategories = {}
    if categories:
        for category in categories:
            subcategories[category] = Subcategory.objects.filter(category_id=category)
    return render(
        request, 
        'cart_detail.html', 
        {
            'cart': cart,
            'categories': categories,
            'subcategories': subcategories,    
        }
    )
