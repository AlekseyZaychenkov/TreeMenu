from django.db import models


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    appsflyer_id = models.CharField(max_length=255)

    install_time = models.CharField(max_length=255)
    event_time = models.CharField(max_length=255)

    campaign = models.CharField(max_length=512)

    platform = models.OneToOneField(Platform, on_delete=models.SET_NULL, null=True)
    media_source = models.CharField(max_length=512)

    event_revenue = models.CharField(max_length=255)
    event_revenue_usd = models.CharField(max_length=255)


class Install(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    appsflyer_id = models.CharField(max_length=255)

    event_time = models.CharField(max_length=255)

    campaign = models.CharField(max_length=512)

    platform = models.OneToOneField(Platform, on_delete=models.SET_NULL, null=True)
    media_source = models.CharField(max_length=512)

    event_revenue = models.CharField(max_length=255)
    event_revenue_usd = models.CharField(max_length=255)
