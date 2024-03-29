from django import template
from django.utils.html import escape
from django.contrib.auth.models import User
from django.utils.hashcompat import md5_constructor
from django.contrib.sites.models import Site

from django.conf import settings

import urllib

GRAVATAR_URL_PREFIX = getattr(settings, "GRAVATAR_URL_PREFIX", "http://www.gravatar.com/")
GRAVATAR_DEFAULT_IMAGE = getattr(settings, "GRAVATAR_DEFAULT_IMAGE", "")

register = template.Library()

def get_user(user):
    if not isinstance(user, User):
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            # TODO: make better? smarter? strong? maybe give it wheaties?
            raise Exception, "Bad user for gravatar."
    return user

def gravatar_for_email(email, size=80):
    default_image_url = ""
    if GRAVATAR_DEFAULT_IMAGE != "":
        this_site = Site.objects.get(pk=settings.SITE_ID)
        default_image_url = this_site.domain + GRAVATAR_DEFAULT_IMAGE
    url = "%savatar/%s/?" % (GRAVATAR_URL_PREFIX, md5_constructor(email).hexdigest())
    url += urllib.urlencode({"s": str(size), "default": default_image_url})
    return url

def gravatar_for_user(user, size=80):
    user = get_user(user)
    return gravatar_for_email(user.email, size)

def gravatar_img_for_email(email, size=80):
    url = gravatar_for_email(email, size)
    return """<img src="%s" height="%s" width="%s"/>""" % (escape(url), size, size)

def gravatar_img_for_user(user, size=80):
    user = get_user(user)
    url = gravatar_for_user(user, size)
    return """<img src="%s" alt="Avatar for %s" height="%s" width="%s"/>""" % (escape(url), user.username, size, size)

def gravatar(user, size=80):
    # backward compatibility
    return gravatar_img_for_user(user, size)

register.simple_tag(gravatar)
register.simple_tag(gravatar_for_user)
register.simple_tag(gravatar_for_email)
register.simple_tag(gravatar_img_for_user)
register.simple_tag(gravatar_img_for_email)
