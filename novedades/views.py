from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import NewsItem
from .forms import NewsItemForm

def es_staff(user):
    return user.is_staff

def news_list(request):
    noticias = NewsItem.objects.filter(publicado=True)
    return render(request, 'novedades/lista_de_novedades.html', {'noticias': noticias})

def news_detail(request, pk):
    noticia = get_object_or_404(NewsItem, pk=pk, publicado=True)
    return render(request, 'novedades/novedades_detalles.html', {'noticia': noticia})

@login_required
@user_passes_test(es_staff)
def news_create(request):
    if request.method == 'POST':
        form = NewsItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('novedades:novedades_lista')
    else:
        form = NewsItemForm()
    return render(request, 'novedades/novedades_formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_staff)
def news_update(request, pk):
    noticia = get_object_or_404(NewsItem, pk=pk)
    if request.method == 'POST':
        form = NewsItemForm(request.POST, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('novedades:novedades_detalles', pk=noticia.pk)
    else:
        form = NewsItemForm(instance=noticia)
    return render(request, 'novedades/novedades_formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_staff)
def news_delete(request, pk):
    noticia = get_object_or_404(NewsItem, pk=pk)
    if request.method == 'POST':
        noticia.delete()
        # lo mismo aquí
        return redirect('novedades:novedades_lista')
    return render(request, 'novedades/novedades_confirmar_eliminar.html', {'noticia': noticia})


