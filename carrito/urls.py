from django.urls import path
from . import views

app_name='carrito'

urlpatterns = [
    path('carrito/', views.cart_detail, name='carrito_detalles'),
    path('carrito/agregar/<int:pk>/', views.cart_add, name='cart_add'),
    path('carrito/eliminar/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('carrito/comprar/', views.cart_checkout, name='cart_checkout'),
]