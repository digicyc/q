from django.db import models

class UserProfile(models.Model):
    """
    Extra information to describe a user.
    """
    firstname = models.TextField(max_length=100)
    lastname = models.TextField(max_length=100)
    address1 = models.TextField(max_length=100)
    address2 = models.TextField(max_length=100)
    city = models.TextField(max_length=100, db_index=True)
    state = models.TextField(max_length=100, db_index=True)
    zip = models.TextField(max_length=20)
    country = models.TextField(max_length=20, db_index=True)
    phone1 = models.TextField(max_length=20)
    phone2 = models.TextField(max_length=20)
    website = models.URLField()
    artist_statement = models.TextField()
    program_statement = models.TextField()
    #: Curriculum Vitae
    cv = models.FileField(upload_to="ducks")
    referal = models.TextField(max_length=255)