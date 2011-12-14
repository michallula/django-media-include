# -*- coding: utf-8 -*-
import sys
from django.conf import settings
 
if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        INSTALLED_APPS=[
            'media_include',
        ],
    )
 
from django.test.simple import run_tests
 
def runtests():
    failures = run_tests(('media_include',), verbosity=1, interactive=True)
    sys.exit(failures)
 
if __name__ == '__main__':
    runtests()
