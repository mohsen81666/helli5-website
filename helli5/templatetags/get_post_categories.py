from django.template.defaulttags import register

from postingApp.models import Category


@register.inclusion_tag("post_categories_navbar_items.html")
def get_post_categories():
    categories =  Category.objects.all()
    return { 'categories': categories}
