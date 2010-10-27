from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Represents a user's profile
    """
    user = models.ForeignKey(User, unique=True)
