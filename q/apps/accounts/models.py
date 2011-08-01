import os
import re

import random
import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.hashcompat import sha_constructor

from ebooks.models import FORMAT_CHOICES, Book, Format

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class UserProfile(models.Model):
    """
    Represents a user's profile
    """
    user = models.ForeignKey(User, unique=True)
    kindle_email = models.EmailField(blank=True, default="")
    available_invites = models.IntegerField(default=0)
	
    def _get_librarian(self):
        return bool(self.user.groups.filter(name='Librarian'))
    is_librarian = property(_get_librarian)

    def _get_num_uploaded_books(self):
        return Format.objects.filter(uploaded_by__exact=self.user).values('ebook').distinct().count()
    uploaded_books_count = property(_get_num_uploaded_books)

    def __str__(self):
        return "<UserProfile: %s>" % self.user

    def __unicode__(self):
        return self.__str__()

class UserDownload(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    format = models.CharField(choices=FORMAT_CHOICES, max_length=20)
    download_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: %s - Download: %s" % (self.user, self.book)

    def __unicode__(self):
        return self.__str__()
        
#INVITES!
class InvitationKeyManager(models.Manager):
    def get_key(self, invitation_key):
        # Don't bother hitting database if invitation_key doesn't match pattern.
        if not SHA1_RE.search(invitation_key):
            return None
        
        try:
            key = self.get(key=invitation_key)
        except self.model.DoesNotExist:
            return None
        
        return key
        
    def is_key_valid(self, invitation_key):
        invitation_key = self.get_key(invitation_key)
        return invitation_key and invitation_key.is_usable()

    def create_invitation(self, user):
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        key = sha_constructor("%s%s%s" % (datetime.datetime.now(), salt, user.username)).hexdigest()
        return self.create(from_user=user, key=key)


class InvitationKey(models.Model):
	key = models.CharField(_('invitation key'), max_length=40)
	date_invited = models.DateTimeField(_('date invited'), 
                                        default=datetime.datetime.now)
	from_user = models.ForeignKey(User, 
                                  related_name='invitations_sent')
	registrant = models.ForeignKey(User, null=True, blank=True, 
                                  related_name='invitations_used')
    
	objects = InvitationKeyManager()
    
	def __unicode__(self):
		return u"Invitation from %s on %s" % (self.from_user.username, self.date_invited)
    
	def is_usable(self):
		return self.registrant is None and not self.key_expired()
    
	def key_expired(self):
		expiration_date = datetime.timedelta(days=settings.ACCOUNT_INVITATION_DAYS)
		return self.date_invited + expiration_date <= datetime.datetime.now()
	key_expired.boolean = True
    
	def mark_used(self, registrant):
		self.registrant = registrant
		self.save()
