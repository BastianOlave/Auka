from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from catalogo.models import Product

def _get_cart(request):
    """Devuelve el carrito de la sesión."""
    return request.session.setdefault('cart', {})


def cart_add(request, pk):
    producto = get_object_or_404(Product, pk=pk, activo=True, stock__gt=0)
    cart = _get_cart(request)
    key = str(pk)
    cart[key] = cart.get(key, 0) + 1
    request.session.modified = True
    messages.success(request, 'Producto añadido al carrito.')
    return redirect('carrito:carrito_detalles')


def cart_remove(request, pk):
    cart = _get_cart(request)
    key = str(pk)
    if key in cart:
        del cart[key]
        request.session.modified = True
        messages.info(request, 'Producto eliminado del carrito.')
    return redirect('carrito:carrito_detalles')


def cart_detail(request):
    cart = _get_cart(request)
    product_ids = cart.keys()
    productos = Product.objects.filter(id__in=product_ids)
    items = []
    total = 0

    for producto in productos:
        cantidad = cart[str(producto.id)]
        subtotal = producto.precio * cantidad
        total += subtotal
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    return render(request, 'carrito/carrito_detalles.html', {
        'items': items,
        'total': total,
    })


@login_required
def cart_checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.info(request, 'Tu carrito está vacío.')
        return redirect('catalogo:producto_lista')

    product_ids = cart.keys()
    productos = Product.objects.filter(id__in=product_ids)

    # Comprobar stock
    for producto in productos:
        cantidad = cart[str(producto.id)]
        if producto.stock < cantidad:
            messages.error(request, f'No hay stock suficiente para {producto.nombre}.')
            return redirect('carrito:carrito_detalles')

    # Bajar stock y guardar (afecta catálogo y servicios, porque usan el mismo modelo)
    for producto in productos:
        cantidad = cart[str(producto.id)]
        producto.stock -= cantidad
        producto.save()  # aquí se desactiva si el stock llega a 0

    # Enviar correo de notificación
    try:
        subject = 'Nueva compra en Auka Terapias'
        message_lines = [
            f'Cliente: {request.user.get_username()}',
            '',
            'Productos comprados:',
        ]
        for producto in productos:
            cantidad = cart[str(producto.id)]
            message_lines.append(f'- {producto.nombre} x {cantidad}')

        message = '\n'.join(message_lines)

        send_mail(
            subject,
            message,
            getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            [getattr(settings, 'DEFAULT_FROM_EMAIL', None)],
            fail_silently=True,
        )
        messages.success(request, 'Compra realizada. Se ha enviado un correo notificando la compra.')
    except Exception:
        messages.success(request, 'Compra realizada. (El correo no pudo enviarse, revisa la configuración de email).')

    # Vaciar carrito
    request.session['cart'] = {}
    request.session.modified = True

    return redirect('catalogo:producto_lista')
