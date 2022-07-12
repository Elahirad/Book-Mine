from .common import *
import os

DEBUG = True

SECRET_KEY = 'django-insecure-7oeaf8v06tpsd-)st!ifgr)vc(pt_o9jqm#67u-veor$5wtb9b'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'db',
        'PORT': '5432',
    }
}
