import os
import sys
from configparser import ConfigParser

config = ConfigParser()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Build Info
try:
    with open(os.path.join(BASE_DIR, 'build', 'BUILD_INFO'), 'r') as build_info:
        PROJECT_VERSION = build_info.readline().strip()
        PROJECT_NAME = build_info.readline().strip()
except IOError as e:
    PROJECT_VERSION = '0.0.0'
    PROJECT_NAME = 'project'

prod_config_path = '/etc/{0}/{0}.conf'.format(PROJECT_NAME)
local_config_path = os.path.join(BASE_DIR, 'build', 'conf', 'local.conf')
default_config_path = os.path.join(BASE_DIR, 'build', 'conf', 'default.conf')

if os.path.exists(prod_config_path):
    config_path = prod_config_path
elif os.path.exists(local_config_path):
    config_path = local_config_path
else:
    config_path = default_config_path
config.read(config_path)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMINS = (
    ('Егор Комаров', 'geoolekom@gmail.com'),
)

DEBUG = config.getboolean('main', 'DEBUG')
SECRET_KEY = config.get('main', 'SECRET')

ALLOWED_HOSTS = ['*', ]

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
    'polls.apps.PollsConfig',
    'blog.apps.BlogConfig',
    'fin_aid',
    'cycle_storage',
    'notifications.apps.NotificationsConfig',
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
        'ENGINE': config.get('database', 'ENGINE'),
        'NAME': config.get('database', 'NAME'),
        'USER': config.get('database', 'USER'),
        'PASSWORD': config.get('database', 'PASSWORD'),
        'HOST': config.get('database', 'HOST'),
        'PORT': config.getint('database', 'PORT'),
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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media', '')
SENDFILE_ROOT = MEDIA_ROOT
FILE_UPLOAD_PERMISSIONS = 0o644

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/'

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
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
        }
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
        }
    }
}


# Messages
VK_GROUP_ID = config.get('messages', 'VK_GROUP_ID')
VK_MESSAGES_TOKEN = config.get('messages', 'VK_MESSAGES_TOKEN')

# Social Auth
SOCIAL_AUTH_VK_OAUTH2_KEY = config.get('oauth', 'VK_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = config.get('oauth', 'VK_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config.get('oauth', 'GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config.get('oauth', 'GOOGLE_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = config.get('oauth', 'GOOGLE_WHITELIST').split(', ')
