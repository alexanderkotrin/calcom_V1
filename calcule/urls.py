from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cpi_book_price/', views.cpi_book_price_calculator, name='cpi_book_price'),
    path('shipping/', views.shipping_calculator, name='shipping'),
    path('order/', views.order_calculator, name='order'),
    path('weight/', views.weight_calculator, name='weight'),  # This line is likely the problem
]
