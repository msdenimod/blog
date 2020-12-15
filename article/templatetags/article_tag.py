from django import template
from article.models import Category

register = template.Library()


@register.inclusion_tag('article/tags/categories_list.html')
def get_categories():
    """Категории"""
    categories = Category.objects.filter(parent__isnull=True)
    return {'categories_list': categories}
