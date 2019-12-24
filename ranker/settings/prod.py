""" Production Settings """
import os
import dj_database_url
from .dev import *


DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}
DEBUG = bool(os.getenv('RANKER_DEBUG', ''))
SECRET_KEY = os.getenv('RANKER_SECRET_KEY', SECRET_KEY)

# Set to your Domain here
ALLOWED_HOSTS = ['*']
