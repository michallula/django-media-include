# -*- coding: utf-8 -*-
from django.conf import settings as django_settings

def get_config(param, *args):    
    if hasattr(django_settings, param):
        return getattr(django_settings, param)
    if args:
        return args[0]
    raise AttributeError, u'{0} setting not specified'.format(param)

MEDIA_CLASS = get_config('MEDIA_INCLUDE_MEDIA_CLASS', 'media_include.media.Media')

MEDIA_CONTEXT_KEY = get_config('MEDIA_INCLUDE_MEDIA_CONTEXT_KEY', 'media_context')
