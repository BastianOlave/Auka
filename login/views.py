from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm


class CustomLoginView(LoginView):
    template_name = 'login/login.html'
    authentication_form = LoginForm
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Si es staff, lo mandamos al panel, si no, al home.
            if request.user.is_staff:
                return redirect('core:panel')
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)
    # ------------------------------------------

    def form_valid(self, form):
        # Recordar sesión
        remember = self.request.POST.get('remember_me') == 'on'
        if remember:
            self.request.session.set_expiry(60 * 60 * 24 * 30)  # 30 días
        else:
            self.request.session.set_expiry(0)  # hasta cerrar navegador
        return super().form_valid(form)

    def get_success_url(self):
        """
        Si es staff → panel.
        Si es cliente → página pública (home).
        """
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('core:panel')   # panel_admin_simple
        return reverse_lazy('core:home')


def register_view(request):
    """
    Registro solo de CLIENTES.
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('core:panel')
        return redirect('core:home')
    # --------------------------------------------

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()   # se guarda ya como cliente (no staff)
            login(request, user)
            # Cliente solo ve la página pública
            return redirect('core:home')
    else:
        form = RegisterForm()
    return render(request, 'login/register.html', {'form': form})


def logout_view(request):
    """Cerrar sesión y volver a la página de inicio."""
    logout(request)
    return redirect('core:home')