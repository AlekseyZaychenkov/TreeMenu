from django import forms
import logging

from django.db.models import Sum, DecimalField, Count
import datetime

from collector.csv_loader import PurchaseLoader, InstallLoader
from collector.models import Platform, MediaSource, Purchase, Install, Result

ALL_NAME = "all"

log = logging.getLogger(__name__)


class DownloadFilesForm(forms.Form):

    purchases_file = forms.FileField(required=False)
    installs_file = forms.FileField(required=False)

    def load(self):
        p_loader = PurchaseLoader()
        p_loader.load(self.cleaned_data["purchases_file"])
        i_loader = InstallLoader()
        i_loader.load(self.cleaned_data["installs_file"])


class NewTableSettingsForm(forms.Form):
    start_date = forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"], required=True)
    end_date = forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"], required=True)
    platform = forms.ModelChoiceField(queryset=Platform.objects.all())
    media_source = forms.ModelChoiceField(queryset=MediaSource.objects.all())

    def calculate(self):
        Result.objects.all().delete()
        log.info(f"Started creating of new result table.")
        purchases = Purchase.objects.filter(
            event_time__range=[self.cleaned_data["start_date"], self.cleaned_data["end_date"]]
        )
        if self.cleaned_data["platform"].name != ALL_NAME:
            platform = Platform.objects.get(platform_id=self.cleaned_data["platform"].platform_id)
            purchases = purchases.filter(platform=platform)
        if self.cleaned_data["platform"].name != ALL_NAME:
            media_source = MediaSource.objects.get(media_source_id=self.cleaned_data["media_source"].media_source_id)
            purchases = purchases.filter(media_source=media_source)

        log.info(f"'{purchases.count()}' purchases from set time period, platform and media source were found.")
        purchase_count = 0
        for row in purchases.values():
            if Result.objects.filter(campaign_id=row['campaign_id']).exists():
                result = Result.objects.filter(campaign_id=row['campaign_id']).get()
                result.sum_revenue_by_campaign = sum([result.sum_revenue_by_campaign, row['event_revenue']])
                result.sum_revenue_by_campaign_usd = sum([result.sum_revenue_by_campaign_usd, row['event_revenue_usd']])
            else:
                result = Result(campaign_id=row['campaign_id'],
                                sum_install_by_campaign=0,
                                sum_revenue_by_campaign=row['event_revenue'],
                                sum_revenue_by_campaign_usd=row['event_revenue_usd']
                                )
            result.save()
            purchase_count += 1
            if purchase_count % 1000 == 0:
                log.info(f"'{purchase_count}' purchases were analyzed.")
        log.info(f"'{purchase_count}' purchases totally were analyzed.")

        installs = Install.objects.filter(
            event_time__range=[self.cleaned_data["start_date"], self.cleaned_data["end_date"]]
        )
        if self.cleaned_data["platform"].name != ALL_NAME:
            platform = Platform.objects.get(platform_id=self.cleaned_data["platform"].platform_id)
            installs = installs.filter(platform=platform)
        if self.cleaned_data["platform"].name != ALL_NAME:
            media_source = MediaSource.objects.get(media_source_id=self.cleaned_data["media_source"].media_source_id)
            installs = installs.filter(media_source=media_source)

        log.info(f"'{installs.count()}' installs from set time period, platform and media source were found.")
        install_count = 0
        for row in installs.values():
            if Result.objects.filter(campaign_id=row['campaign_id']).exists():
                result = Result.objects.filter(campaign_id=row['campaign_id']).get()
                result.sum_install_by_campaign += 1
            else:
                result = Result(campaign_id=row['campaign_id'],
                                sum_install_by_campaign=1,
                                sum_revenue_by_campaign=0,
                                sum_revenue_by_campaign_usd=0)
            result.save()
            install_count += 1
            if install_count % 1000 == 0:
                log.info(f"'{install_count}' installs was analyzed.")
        log.info(f"'{install_count}' installs totally were analyzed.")
