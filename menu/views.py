from django.shortcuts import render
import logging
from menu.models import MenuItem

log = logging.getLogger(__name__)


def home(request):
    context = dict()

    menu_items = set(MenuItem.objects.all())

    child_menu_items = set()
    for item in menu_items:
        if item.parent:
            child_menu_items.add(item)

    context["menu_items"] = child_menu_items
    context["root_menu_items"] = menu_items.difference(child_menu_items)

    return render(request, 'menu/home.html', context)

