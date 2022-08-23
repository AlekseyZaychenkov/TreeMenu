from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MediaSource(models.Model):
    media_source_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    appsflyer_id = models.CharField(max_length=255)

    install_time = models.CharField(max_length=255)
    event_time = models.DateTimeField(max_length=255)

    media_source = models.ForeignKey(MediaSource, on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True)

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

    media_source = models.ForeignKey(MediaSource, on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, null=True)

    event_revenue = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True,
                                        validators=[MinValueValidator(Decimal('0.00'))])
    event_revenue_usd = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True,
                                            validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return self.name



class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    sum_install_by_campaign = models.IntegerField()
    sum_revenue_by_campaign = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True,
                                        validators=[MinValueValidator(Decimal('0.00'))])
    sum_revenue_by_campaign_usd = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True,
                                            validators=[MinValueValidator(Decimal('0.00'))])
