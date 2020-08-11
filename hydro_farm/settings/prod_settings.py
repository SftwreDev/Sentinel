import os
from .common_settings import BASE_DIR

DEBUG = False

ALLOWED_HOSTS = ['hydrofarm.herokuapp.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
