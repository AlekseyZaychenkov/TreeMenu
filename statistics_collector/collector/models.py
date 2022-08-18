from django.db import models


# Create your models here.
class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    appsflyer_id = models.CharField(max_length=255)

    install_time = models.CharField(max_length=255)
    event_time = models.CharField(max_length=255)

    campaign = models.CharField(max_length=512)

    platform = models.CharField(max_length=255)
    media_source = models.CharField(max_length=512)

    event_revenue = models.CharField(max_length=255)
    event_revenue_usd = models.CharField(max_length=255)


class Install(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    appsflyer_id = models.CharField(max_length=255)

    event_time = models.CharField(max_length=255)

    campaign = models.CharField(max_length=512)

    platform = models.CharField(max_length=255)
    media_source = models.CharField(max_length=512)

    event_revenue = models.CharField(max_length=255)
    event_revenue_usd = models.CharField(max_length=255)