from menu.models import MenuItem, Menu
from django.core.exceptions import ValidationError


def validator_that_parent_belongs_to_same_menu(cleaned_data):
    parent = cleaned_data.get("parent")
    menu = cleaned_data.get("menu")
    if parent and menu and parent.menu != menu:
        raise ValidationError("Parent item must belong to same menu!")


def validator_for_unique_url_among_children(cleaned_data):
    parent = cleaned_data.get("parent")
    if parent:
        children = MenuItem.objects.filter(parent=parent)
        children_urls = list(map(lambda child: child.url, children))

        if cleaned_data.get("url") in children_urls:
            raise ValidationError("Url of item should be unique for children of parent item!")


def validator_for_maximum_depth_of_tree(cleaned_data):
    item = cleaned_data.get("parent")
    if item:
        counter = 1
        while item.parent:
            item = item.parent
            counter += 1
            if counter > 10:
                raise ValidationError("Maximum depth of tree should not be more than 10!")


def validator_for_unique_url_among_menus(cleaned_data):
    page = cleaned_data.get("page")
    if page:
        other_menus = Menu.objects.filter(page=page)
        other_menus_urls = list(map(lambda menu: menu.url, other_menus))

        if cleaned_data.get("url") in other_menus_urls:
            raise ValidationError("Url of menu should be unique for menus of the page!")