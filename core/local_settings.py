import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'service.dgap-mipt.ru', 'dev.dgap-mipt.ru']


VK_MESSAGES_TOKEN = "64b717bddbd5890416accb0e67d9a2f9fae28ab8d48f2f65e715318ab1742355cb37df83b3ea7489aca6b"
VK_GROUP_ID = "152995772"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '788072448814-vd0mbulbvrij5pa4ghge0qecuimvur64.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'FB3CCMYctUyKh-A4M-ugQcAf'

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['phystech.edu', 'dgap.mipt.ru']

SOCIAL_AUTH_MIPT_OAUTH2_KEY = 'Vote'
SOCIAL_AUTH_MIPT_OAUTH2_SECRET = '82ASgQEHZbzyxB0gZBp1DJmVH6iV9TG77vJK5KB7xopB2hqMErABOMpn7uEO6WNt'
#SOCIAL_AUTH_VK_OAUTH2_KEY = '5656477'
#SOCIAL_AUTH_VK_OAUTH2_SECRET = '3HabufRwdm5UJaFLcGkb'
SOCIAL_AUTH_VK_OAUTH2_KEY = '5656470'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'kpX3nm0XILGWaGLn6lbE'
