from decimal import Decimal
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash, decorators as dec
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import modelform_factory
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, reverse
from django.template.defaulttags import register
from django.views import generic
from cart.cart import Cart
from cart.forms import CartAddProductForm
from home.forms import UserLoginForm, UserRegisterForm, UserEditForm, CommentForm
from home.models import User, Brand, Category, Comment, MadeIn, Product, Subcategory 
from orders.models import Order, OrderItem



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
        name_filter = 'Подкатегория: ' + subcategory.name
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
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            print('\n\n', comment.text, '\n\n')
            comment.save()
            return HttpResponseRedirect(request.path)
    else:
        form = CommentForm()
    return render(
        request,
        'home/detail.html',
        {
            'form': form,
            'product': product,
            'comments': comments,
            'categories': categories,
            'subcategories': subcategories,
            'cart_product_form': cart_product_form,
        }
    )


def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('home_view'))
    context = {
        'form': UserLoginForm(),
        'cart': Cart(request),
    }
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(reverse('home_view'))
        else:
            context.update(form=form)
    return render(
        request,
        'home/login.html',
        context
    )


@dec.login_required(login_url='login/')
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') if request.META.get('HTTP_REFERER') is not None else redirect(reverse('home_view')))


def register_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('home_view'))
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            if form.cleaned_data['role'] == 'u':
                new_user.is_moderated = True
                new_user.save()
            elif form.cleaned_data['role'] == 's':
                new_user.is_moderated = False
                new_user.is_active = False
                new_user.is_staff = True
                new_user.save()
                group = Group.objects.get(name='sallers')
                new_user.groups.add(group)
            
            return redirect(reverse('login_page'))
    else:
        form = UserRegisterForm()
    return render(
        request,
        'home/register.html',
        {
            'form': form,
            'cart': Cart(request),
        }    
    )


def account_page(request, username):
    flag = False
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=username)
        if request.method == "POST":
            Form = modelform_factory(
                User, form=UserEditForm, fields=('first_name', 'last_name', 'email', 'sex', 'birth_date', 'land', 'city',)
            )
            # form = Form(request.POST, instance=user)
            form = Form(request.POST, instance=user)
            if form.is_valid():
                user_form = form.save(commit=False)
                if form.cleaned_data['password']:
                    user_form.set_password(form.cleaned_data['password'])
                if form.has_changed():
                    flag = True         # Для вывода сообщения об изменении даннных
                    user_form.save()
                    update_session_auth_hash(request, user)
                else:
                    flag = False
        else:
            form = UserEditForm(instance=user)
        dict_orders = {}
        orders = Order.objects.filter(user=user).order_by('-id')
        if Order.objects.filter(user=user).order_by('-id').count() < 10:
            order_count = orders.count()
        else:
            order_count = 10
        orders = Order.objects.filter(user=user).order_by('-id')[:order_count]
        for order in orders:
            list_orders = []
            dict_order = {}
            order_items = OrderItem.objects.filter(order=order)
            for element in order_items:
                product = get_object_or_404(Product, id=element.product_id)
                dict_order['quantity'] = element.quantity
                dict_order['price'] = element.price
                dict_order['total_price'] = element.get_cost()
                dict_order['product_name'] = product.name
                list_orders.append((dict_order['product_name'], dict_order['quantity'], dict_order['price'], dict_order['total_price']))
            dict_orders[order.id] = list_orders
            
        for key, values in dict_orders.items():
            print('\n', key, values, '\n')

        #     for elem, value in orders_items:
                # orders_items.total_price = Decimal(orders_items.price) * Decimal(orders_items.quantity)
        return render(
            request,
            'home/account.html',
            {
                'cart': Cart(request),
                'form': form,
                'username': username,
                'flag': flag,
                'order_count': order_count,
                'dict_orders': dict_orders,
            }
        )
    else:
        return redirect(reverse('home_view'))