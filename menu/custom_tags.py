from django import template
from django.utils.safestring import mark_safe
from menu.models import MenuItem
from menu.utils import is_ancestor

register = template.Library()


def show_item(menu_item: MenuItem, active_menu_item: MenuItem, nesting_depth: int, url: str):
    url += f"/{menu_item.url}"
    descendants_shift = 20
    item_params = "nav-item active" if menu_item == active_menu_item else ""

    text = f"<nav class =\"nav nav-pills ml-3\" >" \
           f"   <a class =\"nav-link {item_params}\" style=\"margin-left:{descendants_shift * nesting_depth}px;\"" \
           f"           href=\"{url}\">" \
           f"       {menu_item.header}" \
           f"   </a> " \
           f"</nav>"

    if menu_item.parent is None or menu_item == active_menu_item or is_ancestor(menu_item, active_menu_item):
        children = MenuItem.objects.filter(parent=menu_item)
        for child in children:
            text += show_item(child, active_menu_item, nesting_depth + 1, url)

    return text


@register.simple_tag()
def show_tree(menu_item, active_menu_item):
    text = show_item(menu_item, active_menu_item, 0, f"/{menu_item.menu.page.url}/{menu_item.menu.url}")
    return mark_safe(text)
