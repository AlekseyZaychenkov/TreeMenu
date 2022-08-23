from django import forms
import logging

from django.db.models import Sum, DecimalField
from django.db.models.functions import Cast

from collector.csv_loader import PurchaseLoader, InstallLoader
from collector.models import Platform, MediaSource, Purchase

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

    start_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=True)
    end_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=True)
    platform = forms.ModelChoiceField(queryset=Platform.objects.all())
    media_source = forms.ModelChoiceField(queryset=MediaSource.objects.all())

    def calculate(self):
        purchases = Purchase.objects.filter(
            event_time__range=[self.cleaned_data["start_date"], self.cleaned_data["end_date"]]
        )
        purchases = Purchase.objects.all()

        # if self.cleaned_data["platform"] != "all":
        #     platform = Platform.objects.get(name=self.cleaned_data["platform"])
        #     purchases = purchases.filter(
        #         # event_time__range=[self.cleaned_data["start_date"], self.cleaned_data["end_date"]],
        #         platform=platform)
        #
        # if self.cleaned_data["platform"] != "all":
        #     media_source = MediaSource.objects.get(name=self.cleaned_data["media_source"])
        #     purchases = purchases.filter(
        #         # event_time__range=[self.cleaned_data["start_date"], self.cleaned_data["end_date"]],
        #         mediasource=media_source)

        log.info(f"purchases.values(): {purchases.values()}")
        for row in purchases.values():
            log.info(f"purchases row: {row}")

        # purchases.group_by = ['campaign']

        # purchases_sum = purchases.aggregate(Sum('campaign'))['column__sum']

        # purchases_sum = purchases.aggregate(event_revenue=Sum('event_revenue'))

        purchases_sum = purchases.values('campaign').order_by('campaign')\
            .annotate(total_price=Sum('event_revenue'))\
            .annotate(total_price_usd=Sum('event_revenue_usd'))

        # purchases_event_revenue_sum = \
        #     purchases.values('campaign').order_by('campaign').annotate(total_price=Sum('event_revenue'))

        # for k, v in purchases_sum.items():
        #     log.info(f"k: {k}   v:{v}")

        log.info(f"purchases_sum: {purchases_sum}")
        log.info(f"purchases_sum.values(): {purchases_sum.values()}")
        log.info(f"len(purchases_sum): {len(purchases_sum)}")

        for row in purchases_sum.values():
            log.info(f"campaign: {row['campaign']} {row['total_price']} {row['total_price_usd']}")

        # log.info(f"purchases_sum: {purchases_sum.count()}")

        