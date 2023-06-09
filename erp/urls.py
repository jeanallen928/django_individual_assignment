from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('erp/', views.erp, name='erp'),
    path('products/', views.product_create, name='product_create'),
    path('inbounds/', views.inbound_create, name='inbound_create'),
    path('outbounds/', views.outbound_create, name='outbound_create'),
    path('inventory/', views.inventory, name='inventory'),
]
