from django.shortcuts import render
import logging
from collector.forms import DownloadFilesForm, NewTableSettingsForm
from collector.models import Purchase, Install

log = logging.getLogger(__name__)


def index(request):
    context = dict()

    if request.POST:
        if request.POST['action'] == 'download_files':
            form = DownloadFilesForm(request.POST)
            if form.is_valid():
                form.load()
            else:
                log.error(form.errors.as_data())

    context["download_files_form"] = DownloadFilesForm()
    context["new_table_settings_form"] = NewTableSettingsForm()

    context["number_of_purchases"] = Purchase.objects.count()
    context["number_of_installs"] = Install.objects.count()


    return render(request, 'collector/index.html', context)
