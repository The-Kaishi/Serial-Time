from django import template
from serials.models import Category, Serial


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('serials/tags/last_serials.html')
def get_last_serials(count=5):
    serials = Serial.objects.order_by('-id')[:count]
    return {'last_serials': serials}
