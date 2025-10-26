from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from .models import Userprofile

from store.forms import ProductForm
from store.models import Product, Order, OrderItem

def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products= user.products.filter(status=Product.ACTIVE)

    return render(request, 'userprofile/vendor_detail.html', {'user': user, 'products': products,})

@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    orders_items = OrderItem.objects.filter(product__user=request.user)

    return render(request, 'userprofile/my_store.html', {'products': products,
    'orders_items': orders_items,})

@login_required
def my_store_order_detail(request, pk):
    order= get_object_or_404(Order, pk=pk)

    return render(request, 'userprofile/my_store_order_detail.html', {
        'order':order
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title= request.POST.get('title')

            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title) 
            product.save()

            messages.success(request, 'The Product was added')

            return redirect('my_store')
        
    else:
        form= ProductForm()
    
    return render(request, 'userprofile/product_form.html', {'title': 'Add product', 'form':form})

@login_required
def edit_product(request, pk):
    product= Product.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, 'Product updated')

            return redirect('my_store')
    else:
        form = ProductForm(instance=product)

        return render(request, 'userprofile/product_form.html', {'title': 'Edit product', 'product': product, 'form':form})

@login_required
def delete_product(request, pk):
    product= Product.objects.filter(user=request.user).get(pk=pk)
    product.status= Product.DELETED
    product.save()

    messages.success(request, 'Product deleted')

    return redirect('my_store')


@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        

        if form.is_valid():
            user= form.save()
            role = form.cleaned_data['role']

            
            user.userprofile.role = role
            user.userprofile.save()

            login(request, user)

            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })


