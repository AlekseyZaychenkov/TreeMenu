from django.shortcuts import render
import logging
from collector.forms import DownloadFilesForm, NewTableSettingsForm
from collector.models import Purchase, Install, Platform, MediaSource, Result

log = logging.getLogger(__name__)


def index(request):
    context = dict()

    if request.POST:
        if request.POST['action'] == 'download_files':
            form = DownloadFilesForm(request.POST, request.FILES)
            if form.is_valid():
                form.load()
            else:
                log.error(form.errors.as_data())
        elif request.POST['action'] == 'calculate_table':
            form = NewTableSettingsForm(request.POST, request.FILES)
            if form.is_valid():
                form.calculate()
            else:
                log.error(form.errors.as_data())

    if not Platform.objects.filter(name="all").exists():
        Platform(name="all").save()
    if not MediaSource.objects.filter(name="all").exists():
        MediaSource(name="all").save()

    context["download_files_form"] = DownloadFilesForm()
    context["new_table_settings_form"] = NewTableSettingsForm()

    context["number_of_purchases"] = Purchase.objects.count()
    context["number_of_installs"] = Install.objects.count()

    context["result_table"] = Result.objects.all()

    return render(request, 'collector/index.html', context)
