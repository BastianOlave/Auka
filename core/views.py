from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from catalogo.models import Product
from novedades.models import NewsItem

def home(request):
    productos_destacados = Product.objects.filter(activo=True, stock__gt=0)[:3]
    noticias_recientes = NewsItem.objects.filter(publicado=True)[:3]
    return render(request, 'core/home.html', {
        'productos_destacados': productos_destacados,
        'noticias_recientes': noticias_recientes,
    })

def es_staff(user):
    return user.is_staff


@login_required
@user_passes_test(es_staff)
def panel(request):
    return render(request, 'core/panel.html')