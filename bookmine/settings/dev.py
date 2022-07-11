from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-7oeaf8v06tpsd-)st!ifgr)vc(pt_o9jqm#67u-veor$5wtb9b'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}