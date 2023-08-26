from django import template
from django.db.models import Count

from men.models import *
from django.core.cache import cache

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('men/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('men'))
            cache.set('cats', cats, 60)
    else:
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('men'))
            cache.set('cats', cats, 60)

    return {'cats': cats, "cat_selected": cat_selected}

