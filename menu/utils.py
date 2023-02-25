from menu.models import MenuItem


def is_ancestor(menu_item_1: MenuItem, menu_item_2: MenuItem):
    if not menu_item_1 or not menu_item_2:
        return False

    current_menu_item = menu_item_2.parent
    while True:
        if not current_menu_item or current_menu_item.id == menu_item_1.id:
            return True
        if current_menu_item.parent:
            current_menu_item = current_menu_item.parent
        else:
            return False


def is_right_ancestor_urls(ancestor_urls: tuple, item_url):
    current_item = MenuItem.objects.get(url=item_url)
    for url in ancestor_urls:
        if url and current_item.parent:
            parent = current_item.parent
            if parent.url != url:
                return False
            else:
                current_item = parent
    return True
