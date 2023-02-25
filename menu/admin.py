from django.contrib import admin
from menu.forms import MenuItemForm, MenuForm
from menu.models import Menu, MenuItem, Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('get_header_with_id', 'url')

    @admin.display()
    def get_header_with_id(self, obj):
        return f"{obj.header} (id='{obj.id}')"


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('get_header_with_id', 'page', 'url')
    form = MenuForm

    @admin.display()
    def get_header_with_id(self, obj):
        return f"{obj.header} (id='{obj.id}')"


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('get_header_with_id', 'url', 'parent', 'menu', 'text')
    form = MenuItemForm

    @admin.display()
    def get_header_with_id(self, obj):
        return f"{obj.header} (id='{obj.id}')"
