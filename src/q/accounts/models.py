from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

from q.ebooks.models import FORMAT_CHOICES, Book, Format

class UserProfile(models.Model):
    """
    Represents a user's profile
    """
    user = models.ForeignKey(User, unique=True)
    kindle_email = models.EmailField(blank=True, default="")

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
