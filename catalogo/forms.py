from django import forms
from .models import Product, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # Ajusta estos campos según tu modelo Category
        fields = ['tipo', 'nombre', 'descripcion']
        # si tu Category tiene otros campos, añádelos aquí


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['tipo', 'categoria', 'nombre', 'descripcion', 'precio', 'imagen', 'stock', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # por defecto, vacío: el JS y el POST lo rellenan
        self.fields['categoria'].queryset = Category.objects.none()

        # cuando viene de un POST, filtramos por tipo
        if 'tipo' in self.data:
            tipo = self.data.get('tipo')
            self.fields['categoria'].queryset = Category.objects.filter(tipo=tipo)
        elif self.instance and self.instance.pk:
            tipo = self.instance.tipo
            self.fields['categoria'].queryset = Category.objects.filter(tipo=tipo)
