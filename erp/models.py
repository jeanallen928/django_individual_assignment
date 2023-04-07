from django.db import models


class Product(models.Model):
    """
    상품 모델입니다.
    상품 코드, 상품 이름, 상품 설명, 상품 가격, 사이즈 필드를 가집니다.
    """
    class Meta:
        db_table = "my_products"

    code = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=256, default='')
    price = models.CharField(max_length=20, null=False)
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=1)
    """
    choices 매개변수는 Django 모델 필드에서 사용하는 매개변수 중 하나로 
    해당 필드에서 선택 가능한 옵션을 지정하는 역할을 합니다. 
    변수를 통해 튜플 리스트를 받으면 첫번째 요소는 실제 DB에 저장되는 값이 되고,
    두번째 요소는 사용자가 볼 수 있는 레이블(옵션의 이름)이 됩니다.
    """

    def __str__(self):
        return self.code

    # def save(self, *args, **kwargs):
    #     # 생성될 때 stock quantity를 0으로 초기화 로직


class Inbound(models.Model):
    """
    입고 모델입니다.
    상품, 수량, 입고 날짜, 금액 필드를 작성합니다.
    """
    class Meta:
        db_table = "inbound"

    code_inbound = models.CharField(max_length=20, null=False)
    quantity = models.IntegerField(default=0)
    inbound_date = models.DateField(auto_now_add=True)
    price_inbound = models.DecimalField(max_digits=19, decimal_places=0, default=0)

