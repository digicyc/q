from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Represents a user's profile
    """
    user = models.ForeignKey(User, unique=True)
    kindle_email = models.EmailField(blank=True, default="")

    def __str__(self):
        return "<UserProfile: %s>" % self.user

    def __unicode__(self):
        return self.__str__()
