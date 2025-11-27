from django.db import models


class Category(models.Model):
    TIPO_CHOICES = (
        ('catalogo', 'Catálogo'),
        ('servicio', 'Servicio'),
    )

    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return f'{self.nombre} ({self.get_tipo_display()})'


class Product(models.Model):
    TIPO_CHOICES = Category.TIPO_CHOICES

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='catalogo')
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Si no hay stock, se desactiva solo
        if self.stock <= 0:
            self.activo = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
