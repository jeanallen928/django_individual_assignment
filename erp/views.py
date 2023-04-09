from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Inbound, Outbound
from django.db import transaction
from django.db.models import Sum


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/products')
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
    all_products = Product.objects.all()
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'erp/product_create.html', {'product': all_products})
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
        return render(request, 'erp/product_create.html', {'product': all_products})


@login_required
@transaction.atomic
def inbound_create(request):
    # 상품 입고 view
    if request.method == 'GET':  # 요청하는 방식이 GET 방식인지 확인하기
        user = request.user.is_authenticated  # 사용자가 로그인이 되어 있는지 확인하기
        total_quantity = Inbound.objects.aggregate(Sum('quantity'))

        # jean_quantity = Inbound.objects.filter(code_inbound='jean-001').aggregate(Sum('quantity'))
        if user:  # 로그인 한 사용자라면
            all_inbounds = Inbound.objects.all().order_by('-inbound_date')
            code_inbound_list = Inbound.objects.distinct().values('code_inbound')
            code_quantity_dict = {}
            for code_ib in code_inbound_list:
                # item_code = code_ib.values()
                item_code = code_ib.get('code_inbound')
                ib_quantity = Inbound.objects.filter(code_inbound=item_code).aggregate(Sum('quantity'))
                # quantity_inbound_list.append(ib_quantity.get('quantity__sum'))
                code_quantity_dict[item_code] = ib_quantity.get('quantity__sum')

            return render(request, 'erp/inbound_create.html', {'inbound': all_inbounds,
                                                               'total_quantity': total_quantity.get('quantity__sum'),
                                                               'code_quantity_dict': code_quantity_dict})
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


@login_required
def outbound_create(request):
    all_outbounds = Outbound.objects.all().order_by('-date_outbound')
    total_quantity = Outbound.objects.aggregate(Sum('quantity_outbound'))

    ib_code_inbound_list = Inbound.objects.distinct().values('code_inbound')
    ib_code_quantity_dict = {}
    for code_ib in ib_code_inbound_list:
        ib_item_code = code_ib.get('code_inbound')
        ib_quantity = Inbound.objects.filter(code_inbound=ib_item_code).aggregate(Sum('quantity')).get('quantity__sum')
        ib_code_quantity_dict[ib_item_code] = ib_quantity

    ob_code_outbound_list = Outbound.objects.distinct().values('code_outbound')
    ob_code_quantity_dict = {}
    for code_ob in ob_code_outbound_list:
        ob_item_code = code_ob.get('code_outbound')
        ob_quantity = Outbound.objects.filter(code_outbound=ob_item_code).aggregate(Sum('quantity_outbound')).get('quantity_outbound__sum')
        ob_code_quantity_dict[ob_item_code] = ob_quantity

    # 상품 출고 view
    if request.method == 'GET':  # 요청하는 방식이 GET 방식인지 확인하기
        user = request.user.is_authenticated  # 사용자가 로그인이 되어 있는지 확인하기
        total_quantity = Outbound.objects.aggregate(Sum('quantity_outbound')).get('quantity_outbound__sum')

        if user:  # 로그인 한 사용자라면
            return render(request, 'erp/outbound_create.html', {'outbound': all_outbounds,
                                                                'total_quantity': total_quantity,
                                                                'code_quantity_dict': ob_code_quantity_dict})
        else:  # 로그인이 되어 있지 않다면
            return redirect('/sign-in')
    # 출고 기록 생성
    elif request.method == 'POST':  # 요청 방식이 POST 일때

        check_ob_code = request.POST.get('code_outbound', '')
        check_ib_quantity = Inbound.objects.filter(code_inbound=check_ob_code).aggregate(Sum('quantity'))
        check_ob_quantity_old = Outbound.objects.filter(code_outbound=check_ob_code).aggregate(Sum('quantity_outbound'))
        check_ob_quantity_new = request.POST.get('quantity_outbound', '')
        if check_ib_quantity.get('quantity__sum') - (check_ob_quantity_old.get('quantity_outbound__sum') + int(check_ob_quantity_new)) < 0:
            return render(request, 'erp/outbound_create.html', {'outbound': all_outbounds,
                                                                'total_quantity': total_quantity.get('quantity_outbound__sum'),
                                                                'code_quantity_dict': ob_code_quantity_dict,
                                                                'error': '재고가 부족합니다.'})
        else:
            my_outbound = Outbound()
            my_outbound.code_outbound = request.POST.get('code_outbound', '')
            my_outbound.quantity_outbound = request.POST.get('quantity_outbound', '')
            my_outbound.price_outbound = request.POST.get('price_outbound', '')
            my_outbound.save()
            return redirect('/outbounds')
    # 재고 수량 조정
    # return render(request, 'erp/outbound_create.html')
    # request.POST.get('code_outbound', '')

@login_required
def inventory(request):
    """
    inbound_create, outbound_create view에서 만들어진 데이터를 합산합니다.
    Django ORM을 통하여 총 수량, 가격등을 계산할 수 있습니다.
    """
# 총 입고 수량, 가격 계산
    total_inbound_quantity = Inbound.objects.aggregate(Sum('quantity')).get('quantity__sum')
    total_inbound_price = Inbound.objects.aggregate(Sum('price_inbound')).get('price_inbound__sum')

# 총 출고 수량, 가격 계산
    total_outbound_quantity = Outbound.objects.aggregate(Sum('quantity_outbound')).get('quantity_outbound__sum')
    total_outbound_price = Outbound.objects.aggregate(Sum('price_outbound')).get('price_outbound__sum')

    all_product = Product.objects.all()
    ib_code_inbound_list = Inbound.objects.distinct().values('code_inbound')
    ob_code_outbound_list = Outbound.objects.distinct().values('code_outbound')
    inventory_item_quantity = {}

    ib_code_inbound_list_real = []
    for i in range(len(ib_code_inbound_list)):
        ib_code_inbound_list_real.append(ib_code_inbound_list[i]['code_inbound'])

    ob_code_outbound_list_real = []
    for i in range(len(ob_code_outbound_list)):
        ob_code_outbound_list_real.append(ob_code_outbound_list[i]['code_outbound'])

    for product in all_product:

        if product.code in ib_code_inbound_list_real:
            ib_quantity = Inbound.objects.filter(code_inbound=product.code).aggregate(Sum('quantity')).get('quantity__sum')
            if product.code in ob_code_outbound_list_real:
                ob_quantity = Outbound.objects.filter(code_outbound=product.code).aggregate(Sum('quantity_outbound')).get('quantity_outbound__sum')
                inventory_item_quantity[product.code] = ib_quantity - ob_quantity
            else:
                inventory_item_quantity[product.code] = ib_quantity
        else:
            inventory_item_quantity[product.code] == 0

    return render(request, 'erp/inventory.html', {'total_inbound_quantity': total_inbound_quantity,
                                                  'total_outbound_quantity': total_outbound_quantity,
                                                  'total_inbound_price': total_inbound_price,
                                                  'total_outbound_price': total_outbound_price,
                                                  'inventory_item_quantity': inventory_item_quantity})







