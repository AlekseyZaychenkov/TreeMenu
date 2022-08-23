from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    appsflyer_id = models.CharField(max_length=255)

    install_time = models.CharField(max_length=255)
    event_time = models.DateTimeField(max_length=255)

    campaign = models.CharField(max_length=512)

    event_revenue = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True,
                                        validators=[MinValueValidator(Decimal('0.00'))])
    event_revenue_usd = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True,
                                            validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return self.name


class Install(models.Model):
    install_id = models.AutoField(primary_key=True)
    appsflyer_id = models.CharField(max_length=255)

    event_time = models.DateTimeField(max_length=255)

    campaign = models.CharField(max_length=512)

    event_revenue = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True,
                                        validators=[MinValueValidator(Decimal('0.00'))])
    event_revenue_usd = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True,
                                            validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return self.name


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    install = models.ForeignKey(Install, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class MediaSource(models.Model):
    media_source_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    install = models.ForeignKey(Install, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    campaign = models.CharField(max_length=512)
    sum_install_by_campaign = models.CharField(max_length=512)
    sum_revenue_by_campaign = models.CharField(max_length=512)
    sum_revenue_by_campaign_usd = models.CharField(max_length=512)
