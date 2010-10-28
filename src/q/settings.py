DEBUG = True
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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'h!pvs80$(+^8%cq63d3npy1+rntpo^(-hkt)_t*2=-kf4hpa6@'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
)

DEFAULT_FILE_STORAGE="amazons3.django.S3Storage"

S3_SETTINGS = {
    'bucket': 'zzq',
    'default_perm': 'public-read',
    'vanity_url': False
}

ROOT_URLCONF = 'q.urls'

TEMPLATE_DIRS = (
        '/home/jason/sites/q.zzq.org/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'q.ebooks',
    'q.accounts',
    'south',
)

AUTH_PROFILE_MODULE = 'accounts.userprofile'

LOGIN_URL = LOGIN_REDIRECT_URL="/login/"

try:
    from local_settings import *
except:
    pass
