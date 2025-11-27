from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mensaje = form.save()
            # Envío de correo simple (a consola por defecto)
            subject = f'Nuevo mensaje de contacto de {mensaje.nombre}'
            body = f"Nombre: {mensaje.nombre}\nCorreo: {mensaje.correo}\n\nMensaje:\n{mensaje.mensaje}"
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
            messages.success(request, 'Tu mensaje ha sido enviado correctamente.')
            return redirect('contacto:contact')
    else:
        form = ContactForm()
    return render(request, 'contacto/contact.html', {'form': form})
