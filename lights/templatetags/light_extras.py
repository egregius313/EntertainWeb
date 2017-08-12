from django.template.defaulttags import register


@register.filter
def item_macro(dictionary):
    return dictionary.items()
