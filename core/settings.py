
"""
Django settings for core project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# WARNING override it in local_settings!
ADMINS = (
    ('DGAP_Voting Admins', 'levyi@email.com'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gp9e%(8c5)^-738+ha==f1-&3j8@3@xpruk)1cxvfsg@%35f8@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['canetoad.mooo.com', 'vote.dgap-mipt.ru']


# Application definition

INSTALLED_APPS = (
    'flat_responsive',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'registration',
    'bootstrap3',
    'sitetree',
    'dealer',
    'django_select2',
    'raven.contrib.django.raven_compat',
    'ckeditor',
    'core',
    'polls',
    'blog',
    'fin_aid',
    'cycle_storage',
    'notifications',
    'senate',
    'django_user_agents',
    'django_bleach',
    'social_django',
    'servertime',
    'profiles',
    'nested_inline',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.contrib.messages.context_processors.messages',
                'dealer.contrib.django.context_processor',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.vk.VKOAuth2',
    #'profiles.psa.MiptOAuth2',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
SELECT2_CACHE_BACKEND = 'select2'

#BOOTSTRAP3 = {
#    'include_jquery': True,
#}

SENDFILE_BACKEND = 'sendfile.backends.development'

SITE_ID = 2

ACCOUNT_ACTIVATION_DAYS = 7

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # 'social_django.middleware.SocialAuthExceptionMiddleware',
    'profiles.psa.SocialAuthExceptionMiddlewareExtended',
)

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# SECURITY WARNING: don't run with this passwords in production!

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'dgap_voting_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres2014',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}


# Bleach default settings
BLEACH_ALLOWED_TAGS = ['b', 'i', 'u', 's', 'a', 'p', 'div', 'ul', 'li', 'img',
                       'h1', 'h2', 'h3', 'font', 'ol', 'script']

BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style', 'src', 'align']

# Which CSS properties are allowed in 'style' attributes (assuming style is
# an allowed attribute)
BLEACH_ALLOWED_STYLES = ['font-size', 'color', 'height', 'width']

# Strip unknown tags if True, replace with HTML escaped characters if False
BLEACH_STRIP_TAGS = False

# To strip HTML comments, or not to strip?
BLEACH_STRIP_COMMENTS = False


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = "j E Y"
DATETIME_FORMAT = DATE_FORMAT + " G:i"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))
SENDFILE_ROOT = MEDIA_ROOT
STATIC_ROOT = (os.path.join(BASE_DIR, 'static'))
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
FILE_UPLOAD_PERMISSIONS = 0o644

LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['phystech.edu']

SOCIAL_AUTH_LOGIN_ERROR_URL = 'polls:done'

SOCIAL_AUTH_PROTECTED_USER_FIELDS = []

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'profiles.psa.approve_student',
    'profiles.psa.set_middlename',
)

import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': sys.stderr
        },
        'sentry': {
            'level': 'WARNING',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

import raven
# Following code is workaround to allow setting up Django from docs/ subdir
try:
    RELEASE = raven.fetch_git_sha(os.path.dirname(os.pardir))
except raven.exceptions.InvalidGitRepository:
    RELEASE = raven.fetch_git_sha(os.path.abspath('..'))

RAVEN_CONFIG = {
    'dsn': 'https://af8512c3bfe6466e92610a28d10584af:232450226e59481fb4f1020cdaad9d3e@sentry.io/225398',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': RELEASE,
}


from core.local_settings import *
