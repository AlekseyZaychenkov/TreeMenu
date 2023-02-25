from django.db import models


class Page(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=511)
    url = models.CharField(max_length=511)

    def __str__(self):
        return f"{self.header} (id='{self.id}')"


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=511)
    url = models.CharField(max_length=511)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.page:
            return f"{self.header} (id='{self.id}') ({self.page.header})"
        else:
            return f"{self.header} (id='{self.id}') (no page)"


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=511)
    url = models.CharField(max_length=511)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.menu:
            return f"{self.header} (id='{self.id}') ({self.menu.header})"
        else:
            return f"{self.header} (id='{self.id}') (no menu)"
