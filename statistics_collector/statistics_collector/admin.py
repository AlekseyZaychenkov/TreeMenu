from django.contrib import admin
from collector.models import Platform, Purchase, Install


collector_admin = admin.AdminSite()
collector_admin.register(Platform)
collector_admin.register(Purchase)
collector_admin.register(Install)