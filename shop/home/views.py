from django.shortcuts import render, get_object_or_404
from django.views import generic
from home.models import User, Brand, Category, Comment, MadeIn, Product, Subcategory 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register
from cart.forms import CartAddProductForm



@register.filter
def dict_key(dictionary, key):
    return dictionary[key]


def product_list(request, category_slug=None, subcategory_slug=None):
    name_filter = 'Все товары'
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        name_filter = 'Категория: ' + category.name
        object_list = Product.objects.filter(available=True, category=category)
    elif subcategory_slug:
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        name_filter = 'Категория: ' + subcategory.name
        object_list = Product.objects.filter(available=True, subcategory=subcategory)
    else:
        object_list = Product.objects.filter(available=True)
    paginator = Paginator(object_list, 20)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)
    categories = Category.objects.all()
    subcategories = {}
    if categories:
        for category in categories:
            subcategories[category] = Subcategory.objects.filter(category_id=category)
    for product in products:
        if product.discount_price:
            product.discount = 100 - round(product.discount_price * 100 / product.price)
    return render(
        request,
        'home/list.html',
        {
            'name_filter': name_filter,
            'page': page,
            'products': products,
            'categories': categories,
            'subcategories': subcategories,
        }
    )


def product_detail(request, id):
    product = get_object_or_404(
        Product,
        id=id,
        available=True,
    )
    comments = Comment.objects.filter(product=product)
    categories = Category.objects.all()
    subcategories = {}
    if categories:
        for category in categories:
            subcategories[category] = Subcategory.objects.filter(category_id=category)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'home/detail.html',
        {
            'product': product,
            'comments': comments,
            'categories': categories,
            'subcategories': subcategories,
            'cart_product_form': cart_product_form,
        }
    )

