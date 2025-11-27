from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from catalogo.models import Product, Category
from catalogo.forms import ProductForm, CategoryForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse



def es_staff(user):
    return user.is_staff

def product_list(request):
    categoria_id = request.GET.get('categoria')

    productos = Product.objects.filter(
        tipo='catalogo'
    ).select_related('categoria')

    if not request.user.is_staff:
        productos = productos.filter(activo=True, stock__gt=0)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = Category.objects.filter(tipo='catalogo')


    paginator = Paginator(productos, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalogo/producto_lista.html', {
        'productos': page_obj.object_list,
        'page_obj': page_obj,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
    })


def product_detail(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    return render(request, 'catalogo/producto_detalles.html', {'producto': producto})

@login_required
@user_passes_test(es_staff)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogo:producto_lista')
    else:
        # leer el tipo de la query string: ?tipo=catalogo o ?tipo=servicio
        tipo = request.GET.get('tipo')
        initial = {}
        if tipo:
            initial['tipo'] = tipo
        form = ProductForm(initial=initial)

    return render(request, 'catalogo/producto_formulario.html', {
        'form': form,
        'accion': 'Crear',
    })

@login_required
@user_passes_test(es_staff)
def product_update(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('catalogo:producto_detalles', pk=producto.pk)
    else:
        form = ProductForm(instance=producto)
    return render(request, 'catalogo/producto_formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_staff)
def product_delete(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('catalogo:producto_lista')
    return render(request, 'catalogo/producto_confirmacion_eliminar.html', {'producto': producto})

@login_required
@user_passes_test(es_staff)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, 'Categoría creada correctamente.')

            # volvemos a crear producto con ese tipo
            url = reverse_lazy('catalogo:product_create')
            return redirect(f'{url}?tipo={categoria.tipo}')
    else:
        form = CategoryForm()

    return render(request, 'catalogo/categoria_formulario.html', {
        'form': form,
        'accion': 'Crear categoría'
    })

class CategoriaCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalogo/categoria_formulario.html'
    success_url = reverse_lazy('catalogo:product_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Crear categoría'
        return context
    
@login_required
def cargar_categorias(request):
    tipo = request.GET.get('tipo')
    categorias = Category.objects.filter(tipo=tipo).values('id', 'nombre')
    return JsonResponse(list(categorias), safe=False)

@login_required
@user_passes_test(es_staff)
def category_delete(request, pk):
    categoria = get_object_or_404(Category, pk=pk)

    # comprobar si hay productos asociados
    if Product.objects.filter(categoria=categoria).exists():
        messages.error(request, 'No puedes eliminar esta categoría porque tiene productos asociados.')
        return redirect('catalogo:product_create')

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('catalogo:product_create')

    return render(request, 'catalogo/categoria_eliminar.html', {
        'categoria': categoria
    })