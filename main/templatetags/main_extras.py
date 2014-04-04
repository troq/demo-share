from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def progress_percent(value, arg):
    return 100 if value>arg else 100.0*value/arg

@register.filter
def add_real(value, arg):
    return str(Decimal(float(value)+arg).quantize(Decimal('1.00')))
