from django.shortcuts import render
from django.core.paginator import Paginator
from catalogo.models import Product, Category



def servicios(request):
    categoria_id = request.GET.get('categoria')

    servicios_qs = Product.objects.filter(
        tipo='servicio',
        activo=True,
        stock__gt=0,
    ).select_related('categoria')

    if categoria_id:
        servicios_qs = servicios_qs.filter(categoria_id=categoria_id)

    categorias = Category.objects.filter(tipo='servicio')

    paginator = Paginator(servicios_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'servicios/servicios.html', {
        'servicios': page_obj.object_list,
        'page_obj': page_obj,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
    })
