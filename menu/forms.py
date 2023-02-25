from django import forms
from menu.models import Menu, MenuItem, Page
from menu.validators import validator_for_unique_url_among_children, validator_for_maximum_depth_of_tree,\
    validator_that_parent_belongs_to_same_menu, validator_for_unique_url_among_menus


class MenuItemForm(forms.ModelForm):
    header = forms.CharField(max_length=511)
    url = forms.CharField(max_length=511)
    menu = forms.ModelChoiceField(Menu.objects.all(), required=False)
    parent = forms.ModelChoiceField(MenuItem.objects.all(), required=False)
    text = forms.CharField(max_length=10000, widget=forms.Textarea(attrs={"rows": 5, "cols": 150}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        validator_for_unique_url_among_children(cleaned_data)
        validator_that_parent_belongs_to_same_menu(cleaned_data)
        validator_for_maximum_depth_of_tree(cleaned_data)
        return cleaned_data

    class Meta:
        model = MenuItem
        exclude = ['id']


class MenuForm(forms.ModelForm):
    header = forms.CharField(max_length=511)
    url = forms.CharField(max_length=511)
    page = forms.ModelChoiceField(Page.objects.all(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        validator_for_unique_url_among_menus(cleaned_data)
        return cleaned_data

    class Meta:
        model = MenuItem
        exclude = ['id']