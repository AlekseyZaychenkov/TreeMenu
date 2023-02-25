from django.shortcuts import render
import logging
from menu.models import MenuItem
from menu.utils import is_right_ancestor_urls

log = logging.getLogger(__name__)


# TODO: Меню на одной странице может быть несколько. Они определяются по названию.
def home(request, ancestor_url_1=None, ancestor_url_2=None, ancestor_url_3=None, ancestor_url_4=None,
         ancestor_url_5=None, ancestor_url_6=None, ancestor_url_7=None, ancestor_url_8=None, ancestor_url_9=None,
         active_item_url=None):
    context = dict()

    menu_items = set(MenuItem.objects.all())

    child_menu_items = set()
    for item in menu_items:
        if item.parent:
            child_menu_items.add(item)

    context["menu_items"] = child_menu_items
    context["root_menu_items"] = menu_items.difference(child_menu_items)
    
    # TODO: verify ancestors path
    ancestor_urls = (ancestor_url_1, ancestor_url_2, ancestor_url_3, ancestor_url_4, ancestor_url_5, ancestor_url_6,
                     ancestor_url_7, ancestor_url_8, ancestor_url_9)
    context["active_menu_item"] = MenuItem.objects.get(url=active_item_url) \
        if active_item_url and is_right_ancestor_urls(ancestor_urls, active_item_url) else None

    return render(request, 'menu/home.html', context)

