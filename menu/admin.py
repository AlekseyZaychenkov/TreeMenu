from django.contrib import admin
from menu.models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('get_header_with_id', 'url', 'parent', 'text')

    @admin.display()
    def get_header_with_id(self, obj):
        return f"{obj.header} (id='{obj.id}')"
