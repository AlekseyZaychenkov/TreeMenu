from django.shortcuts import render
import logging
from menu.models import Menu, MenuItem, Page
from menu.utils import is_right_ancestor_urls

log = logging.getLogger(__name__)


def home(request, active_page_url=None, active_menu_url=None, ancestor_url_1=None, ancestor_url_2=None,
         ancestor_url_3=None, ancestor_url_4=None, ancestor_url_5=None, ancestor_url_6=None, ancestor_url_7=None,
         ancestor_url_8=None, ancestor_url_9=None, active_item_url=None):
    context = dict()

    context["pages"] = Page.objects.all()

    if active_page_url:
        context["active_page_url"] = active_page_url
        page = Page.objects.get(url=active_page_url)
        menu_to_root_menu_items = dict()
        menus = Menu.objects.filter(page=page)

        for menu in menus:
            menu_items = set(MenuItem.objects.filter(menu=menu))
            child_menu_items = set()
            for item in menu_items:
                if item.parent:
                    child_menu_items.add(item)
            root_menu_items = menu_items.difference(child_menu_items)
            menu_to_root_menu_items[menu] = root_menu_items

        context["menu_to_root_menu_items"] = menu_to_root_menu_items

        ancestor_urls = (ancestor_url_1, ancestor_url_2, ancestor_url_3, ancestor_url_4, ancestor_url_5, ancestor_url_6,
                         ancestor_url_7, ancestor_url_8, ancestor_url_9)
        context["active_menu_item"] = MenuItem.objects.get(url=active_item_url) \
            if active_item_url and is_right_ancestor_urls(ancestor_urls, active_item_url) else None

    return render(request, 'menu/home.html', context)

