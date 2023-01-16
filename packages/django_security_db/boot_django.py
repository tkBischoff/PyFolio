# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
import os
import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "security_db"))

def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default":{
                "ENGINE":"django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(
            'security_db',
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',

        ),
        MIDDLEWARE = [
             'django.middleware.security.SecurityMiddleware',
             'django.contrib.sessions.middleware.SessionMiddleware',
             'django.middleware.common.CommonMiddleware',
             'django.middleware.csrf.CsrfViewMiddleware',
             'django.contrib.auth.middleware.AuthenticationMiddleware',
             'django.contrib.messages.middleware.MessageMiddleware',
             'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()
