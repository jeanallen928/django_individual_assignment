from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/erp')
    else:
        return redirect('/sign-in')


def erp(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'erp/home.html')
        else:
            return redirect('/sign-in')


@login_required
def product_list(request):
    return render(request, 'erp/home.html')


@login_required
def product_create(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'erp/product_create.html')
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        my_product = Product()
        my_product.code = request.POST.get('code')
        my_product.name = request.POST.get('name')
        my_product.size = request.POST.get('size')
        my_product.price = request.POST.get('price')
        my_product.description = request.POST.get('description')
        my_product.save()
        return render(request, 'erp/product_create.html')
