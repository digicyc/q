from django.db import models

class UserProfile(models.Model):
    """
    Extra information to describe a user.
    """
    address1 = models.TextField(max_length=100)
    address2 = models.TextField(max_length=100)
    city = models.TextField(max_length=100)
    state = models.TextField(max_length=100)
    zip = models.TextField(max_length=20)
    country = models.TextField(max_length=20)
    phone1 = models.TextField(max_length=20)
    phone2 = models.TextField(max_length=20)
    website = models.URLField()
    artist_statement = models.TextField()
    program_statement = models.TextField()
    #: Curriculum Vitae
    cv = models.FileField(upload_to="ducks")
    referal = models.TextField(max_length=255)