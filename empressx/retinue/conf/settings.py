"""
empressx.retinue.conf.settings
==============================
"""
from empressx.retinue.conf.defaults import *
from django.conf import settings as django_settings

for setting in dir(django_settings):
    if setting == setting.upper() and setting in locals():
        locals()[setting] = getattr(django_settings, setting)