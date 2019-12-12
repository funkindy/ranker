""" Production Settings """
import os
from .dev import *

DEBUG = bool(os.getenv('RANKER_DEBUG', ''))
SECRET_KEY = os.getenv('RANKER_SECRET_KEY', SECRET_KEY)

# Set to your Domain here
ALLOWED_HOSTS = ['*']