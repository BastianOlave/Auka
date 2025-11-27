from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.product_list, name='producto_lista'),
    path('<int:pk>/', views.product_detail, name='producto_detalles'),
    path('crear/', views.product_create, name='product_create'),
    path('<int:pk>/editar/', views.product_update, name='product_update'),
    path('<int:pk>/eliminar/', views.product_delete, name='product_delete'),
    path('categorias/crear/', views.category_create, name='category_create'),
    path('ajax/cargar-categorias/', views.cargar_categorias, name='cargar_categorias'),
    path('categoria/<int:pk>/eliminar/', views.category_delete, name='categoria_eliminar'),
]