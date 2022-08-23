import logging
import csv
import tempfile
from decimal import Decimal
from abc import ABC, abstractmethod
from typing import Any

from django.core.exceptions import FieldError

from collector.models import Purchase, Platform, Install, MediaSource, Campaign

log = logging.getLogger(__name__)


class CsvLoader(ABC):
    def load(self, uploaded_file):
        log.info(f"Started loading file '{uploaded_file}'")
        count = 0
        existed_count = 0
        err_count = 0


        file_temp = tempfile.NamedTemporaryFile()
        file_temp.write(uploaded_file.read())

        try:
            with open(file_temp.name) as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    try:
                        if MediaSource.objects.filter(name=row['media_source']).exists():
                            media_source = MediaSource.objects.filter(name=row['media_source']).get()
                        else:
                            media_source = MediaSource(name=row['media_source'])
                            media_source.save()

                        if Campaign.objects.filter(name=row['campaign']).exists():
                            campaign = Campaign.objects.filter(name=row['campaign']).get()
                        else:
                            campaign = Campaign(name=row['campaign'])
                            campaign.save()

                        if Platform.objects.filter(name=row['platform']).exists():
                            platform = Platform.objects.filter(name=row['platform']).get()
                        else:
                            platform = Platform(name=row['platform'])
                            platform.save()

                        if self.load_row(row, media_source, campaign, platform):
                            count += 1
                        else:
                            existed_count += 1

                        if count != 0 and count % 1000 == 0:
                            log.info(f"'{count}' new records "
                                     f"was successfully downloaded from file '{uploaded_file}'.")
                        if existed_count != 0 and existed_count % 1000 == 0:
                            log.info(f"'{existed_count}' records from '{uploaded_file}' "
                                     f"already existed in db and were skipped.")

                    except IOError as err:
                        log.error(f"Error occurred during of reading one of rows file '{uploaded_file}':"
                                  f"\n{err}")
                        err_count += 1
                        if err_count != 0 and err_count % 100 == 0:
                            log.error(f"'{err_count}' records didn't downloaded from file '{uploaded_file}'.")

                    except FieldError as err:
                        log.error(f"Error occurred during of saving to db one of rows file '{uploaded_file}':"
                                  f"\n{err}")
                        err_count += 1
                        if err_count != 0 and err_count % 100 == 0:
                            log.error(f"'{err_count}' records didn't downloaded from file '{uploaded_file}'.")

        except IOError as err:
            log.error(f"Error occurred during of reading of file '{uploaded_file}':"
                      f"\n{err}")

        log.info(f"Finished loading file '{uploaded_file}'. "
                 f"'{count}' new records was successfully downloaded, "
                 f"'{existed_count}' records already existed in db and were skipped."
                 f"'{err_count}' records was damaged and don't downloaded.")

    @abstractmethod
    def load_row(self, row, media_source, campaign, platform):
        pass


class PurchaseLoader(CsvLoader):
    def load_row(self, row, media_source, campaign, platform):
        event_revenue = Decimal(row['event_revenue']) if is_float(row['event_revenue']) else 0
        event_revenue_usd = Decimal(row['event_revenue_usd']) if is_float(row['event_revenue_usd']) else 0

        if not Purchase.objects.filter(appsflyer_id=row['appsflyer_id'],
                                       install_time=row['install_time'],
                                       event_time=row['event_time'],
                                       media_source=media_source,
                                       campaign=campaign,
                                       platform=platform,
                                       event_revenue=event_revenue,
                                       event_revenue_usd=event_revenue_usd
                                       ).exists():

            purchase = Purchase(appsflyer_id=row['appsflyer_id'],
                                install_time=row['install_time'],
                                event_time=row['event_time'],
                                media_source=media_source,
                                campaign=campaign,
                                platform=platform,
                                event_revenue=event_revenue,
                                event_revenue_usd=event_revenue_usd
                                )
            purchase.save()
            return True
        else:
            return False


class InstallLoader(CsvLoader):
    def load_row(self, row, media_source, campaign, platform):
        event_revenue = Decimal(row['event_revenue']) if row['event_revenue'].isdecimal() else 0
        event_revenue_usd = Decimal(row['event_revenue_usd']) if row['event_revenue_usd'].isdecimal() else 0

        if not Install.objects.filter(appsflyer_id=row['appsflyer_id'],
                                      event_time=row['event_time'],
                                      media_source=media_source,
                                      campaign=campaign,
                                      platform=platform,
                                      event_revenue=event_revenue,
                                      event_revenue_usd=event_revenue_usd
                                      ).exists():

            install = Install(appsflyer_id=row['appsflyer_id'],
                              event_time=row['event_time'],
                              media_source=media_source,
                              campaign=campaign,
                              platform=platform,
                              event_revenue=event_revenue,
                              event_revenue_usd=event_revenue_usd
                              )
            install.save()
            return True
        else:
            return False


def is_float(element: Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False
