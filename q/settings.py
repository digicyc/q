import os
import os.path
import sys

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('jason', 'jason@zzq.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'q',
        'USER': 'root',
        'HOST': 'localhost',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = "q@zzq.org"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "q@zzq.org"
EMAIL_HOST_PASSWORD = ""
EMAIL_SUBJECT_PREFIX = "[q] "
EMAIL_USE_TLS = True

DEFAULT_HTTP_HEADERS = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Denver'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/'

ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'h!pvs80$(+^8%cq63d3npy1+rntpo^(-hkt)_t*2=-kf4hpa6@'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


if __import__('debug_toolbar'):
    INTERNAL_IPS = ('127.0.0.1', 'tex.ath.cx',)
    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    
#    'ebooks.processors.book_count_insert',
    'ebooks.processors.site_insert',
    'ebooks.processors.version_insert',
    'ebooks.processors.hostname_insert',

)

DEFAULT_FILE_STORAGE="amazons3.django.S3Storage"

S3_SETTINGS = {
    'bucket': 'zzq',
    'default_perm': 'public-read',
    'vanity_url': False
}

ROOT_URLCONF = 'q.urls'

TEMPLATE_DIRS = [
        os.path.join(PROJECT_ROOT, 'templates'),
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.comments',
        
    'ebooks',
    'accounts',

    'south',
    'tagging',
    'activity_stream',
    'threadedcomments',
    'djangoratings',
)

COMMENTS_APP = 'threadedcomments'
GRAVATAR_DEFAULT_IMAGE = '/images/blank-avatar.png'
AUTH_PROFILE_MODULE = 'accounts.userprofile'

# This is mainly for beanstalk to deploy the sites automatically
WSGI_RELOAD_KEY = None
WSGI_RELOAD_PATH = "/home/jason/sites/q.zzq.org/scripts/q.wsgi"

#INVITES
INVITE_MODE = True
ACCOUNT_INVITATION_DAYS = 30

LOGIN_URL = LOGIN_REDIRECT_URL="/login/"

try:
    from local_settings import *
except ImportError:
    pass
