from django.urls import path
from . import views

app_name = 'novedades'

urlpatterns = [
    path('', views.news_list, name='novedades_lista'),
    path('<int:pk>/', views.news_detail, name='novedades_detalles'),
    path('crear/', views.news_create, name='crear_novedades'),
    path('<int:pk>/editar/', views.news_update, name='actualizar_novedades'),
    path('<int:pk>/eliminar/', views.news_delete, name='eliminar_novedades'),
]
