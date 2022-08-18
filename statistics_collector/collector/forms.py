from django import forms
import logging
from collector.csv_loader import load_purchases, load_installs
from collector.utils import get_existing_platforms

log = logging.getLogger(__name__)


class DownloadFilesForm(forms.Form):

    purchases_file = forms.FileField()
    installs_file = forms.FileField()

    def load(self):
        load_purchases(self.data["purchases_file"])
        load_installs(self.data["installs_file"])


class NewTableSettingsForm(forms.Form):

    start_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=True)
    end_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=True)
    platform = forms.ChoiceField(choices=get_existing_platforms())

    def load(self):
        load_purchases(self.data["purchases_file"])
        load_installs(self.data["installs_file"])
