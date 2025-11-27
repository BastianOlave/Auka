from django.db import models

class NewsItem(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-creado_en']

    def __str__(self):
        return self.titulo
