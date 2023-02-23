from django.db import models


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=511)
    url = models.CharField(max_length=511)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.header} (id='{self.id}')"
