import os

# Local settings for Django projects
# Set all values here before starting the project
# Move this file to the same folder as main settings.py file
# Rename the file as local_settings.py

DEBUG = False

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

# Generate a secret key, and don't share it with anybody.
#  from django.utils.crypto import get_random_string
# chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
# get_random_string(50, chars)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k%m(0me09-zyjh32s)2oo8j*_#ivjdoa6jeqmx#(sz+06e2t#8'

# Not required as ngnix does this now
# SECURE_SSL_REDIRECT = True

X_FRAME_OPTIONS = 'DENY'

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = (
    ('FOSS@Amrita', 'amritapurifoss@gmail.com')
)

ADMINS_EMAIL = map(lambda x: x[1], ADMINS)

# Sending email using SMTP gmail server

EMAIL_HOST_USER = 'amritapurifoss@gmail.com'
EMAIL_HOST_PASSWORD = 'password'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'amritapurifoss@gmail.com'
SERVER_EMAIL = 'amritapurifoss@gmail.com'

# If running in debug mode, write emails to files.
if not DEBUG:
    # During development only
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

RECAPTCHA_USE_SSL = True

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        # Database name or path to database file if using sqlite3.
        'NAME': '',
        # Not used with sqlite3.
        'USER': '',
        # Not used with sqlite3.
        'PASSWORD': '',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

EMAIL = 'amritapurifoss@gmail.com'
MAILING_LIST = 'foss-2017@googlegroups.com'
DOMAIN = 'amfoss.in'

# Telegram bot

telegram_bot_token = ''
telegram_group_id = 0

# bcc mail id for join application task mail
join_application_mail_list = []

# mail id to sent task and reply to
join_application_reply_to = []
