from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Inbound
from django.db import transaction
from django.db.models import Sum


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


@login_required
@transaction.atomic
def inbound_create(request):
    # 상품 입고 view
    if request.method == 'GET':  # 요청하는 방식이 GET 방식인지 확인하기
        user = request.user.is_authenticated  # 사용자가 로그인이 되어 있는지 확인하기
        total_quantity = Inbound.objects.aggregate(Sum('quantity'))
        if user:  # 로그인 한 사용자라면
            all_inbounds = Inbound.objects.all().order_by('-inbound_date')
            return render(request, 'erp/inbound_create.html', {'inbound': all_inbounds, 'total_quantity': total_quantity.get('quantity__sum')})
        else:  # 로그인이 되어 있지 않다면
            return redirect('/sign-in')
    # 입고 기록 생성
    elif request.method == 'POST':  # 요청 방식이 POST 일때
        my_inbound = Inbound()
        my_inbound.code_inbound = request.POST.get('code_inbound', '')
        my_inbound.quantity = request.POST.get('quantity', '')
        my_inbound.price_inbound = request.POST.get('price_inbound', '')
        my_inbound.save()
        return redirect('/inbounds')
    # 입고 수량 조정


