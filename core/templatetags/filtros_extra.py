from django import template

register = template.Library()

@register.filter
def clp(value):
    """Convierte un número a formato moneda chilena: 3990 -> $3.990"""
    try:
        value = int(value) # Quitamos decimales (.00)
        return "${:,.0f}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value