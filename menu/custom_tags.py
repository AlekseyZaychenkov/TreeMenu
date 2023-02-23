from django.utils.safestring import mark_safe
from menu.models import MenuItem
from django import template

register = template.Library()


def show_item(menu_item, nesting_depth):

    text = f"<nav class =\"nav nav-pills flex-column ml-3\" >" \
           f"   <a class =\"nav-link\" style=\"margin-left:{20 * nesting_depth}px;\" href=\"#{menu_item.url}\" > " \
           f"       {menu_item.header}" \
           f"   </a> " \
           f"</nav>"

    children = MenuItem.objects.filter(parent=menu_item)

    for child in children:
        text += show_item(child, nesting_depth + 1)

    return text


@register.simple_tag()
def show_tree(menu_item):
    text = show_item(menu_item, 0)
    return mark_safe(text)


# @register.simple_tag(is_safe=True)
