import os
import os.path
import random
from hashlib import sha256 as sha

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files import File

FORMAT_CHOICES = (
    ('doc', 'doc'),
    ('epub', 'epub'),
    ('lit', 'lit'),
    ('mobi', 'mobi'),
    ('pdf', 'pdf'),
    ('rtf', 'rtf'),
    ('txt', 'txt'),
)

def book_save(instance, original_filename):
    extension = os.path.splitext(original_filename)[1].lower()
    filename = generate_book_filename(instance.ebook.title,
            instance.ebook.authors.all()[0], extension)
    return os.path.join("books", "files", filename)

def cover_save(instance, original_filename):
    extension = os.path.splitext(original_filename)[1].lower()
    filename = generate_book_filename(instance.title,
            instance.authors.all()[0], extension)
    return os.path.join("books", "covers", filename)

def thumb_save(instance, original_filename):
    extension = os.path.splitext(original_filename)[1].lower()
    filename = generate_book_filename(instance.title,
            instance.authors.all()[0], extension)
    return os.path.join("books", "covers", filename)

def generate_book_filename(title, author, extension):
    filename = slugify("%s_%s" % (title, author))

    return "%s.%s" % (filename, extension.replace('.', ''))


class Ownership(models.Model):
    user = models.ForeignKey(User, db_index=True )
    book = models.ForeignKey('Book', db_index=True)
    checked_out = models.ForeignKey(User, related_name="checkout_to", null=True, blank=True)
    
    def __str__(self):
        return "%s" % (self.user)
    
    class Meta:
        unique_together = (("user", "book"),)

class Book(models.Model):
    title = models.CharField(db_index=True, max_length=100)
    # m2m in the future
    authors = models.ManyToManyField("Author", blank=True)
    metarating = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    #tags = models.ManyToMany("Tags")
    isbn10 = models.CharField(db_index=True, max_length=20, blank=True)
    isbn13 = models.CharField(db_index=True, max_length=20, blank=True)
    gid = models.CharField(db_index=True, max_length=20, blank=True)
    description = models.TextField(blank=True)
    published = models.DateField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to=cover_save, blank=True)
    thumbnail = models.ImageField(upload_to=thumb_save, blank=True)
    slug = models.SlugField(max_length=255, blank=True, db_index=True)
    is_physical = models.BooleanField(default=False)
    is_ebook = models.BooleanField(default=False)
    checked_out = models.ForeignKey(User, null=True, blank=True, related_name="checked_out")
    key = models.CharField(max_length=30, blank=True, db_index=True)
    owners = models.ManyToManyField(Ownership, related_name="owners", blank=True)

    def _get_categories(self):
        return Category.objects.filter(books=self)
    categories = property(_get_categories)

    def __str__(self):
        return "%s" % (self.title)

    def _get_formats(self):
        return Format.objects.filter(ebook=self).order_by('format')
    formats = property(_get_formats)

    def show_qr_code(self):
        current_site = Site.objects.get_current()
        img_size = "140x140"
        url = "http://chart.apis.google.com/chart?chs="+img_size+"&cht=qr&chl="
        url += current_site.name+"/books/checkout/"+self.key
        url += "&choe=UTF-8"

        return "<img src='"+url+"' />"

    def cache_book_info(self, gid=None):
        import urllib2
        from tempfile import NamedTemporaryFile

        from gdata.books import Book as GBook

        if gid is None:
            gid = self.gid

        if gid is None:
            return

        volume_xml = urllib2.urlopen("http://www.google.com/books/feeds/volumes/%s" % gid).read()
        gbook = GBook.FromString(volume_xml)

        thumbnail_link = gbook.GetThumbnailLink().href
        cover_link = gbook.GetThumbnailLink().href.replace('zoom=5','zoom=1')

        if self.title == "":
            self.title = gbook.title.text

        if gbook.rating is not None:
            self.metarating = gbook.rating.average

        if gbook.description is not None and self.description == "":
            self.description = gbook.description.text
        self.published_year = gbook.date.text

        for gauthor in gbook.creator:
            gauthor = gauthor.text
            try:
                author = Author.objects.get(firstname=" ".join(gauthor.split(" ")[:-1]).strip(), lastname=gauthor.split(" ")[-1])
            except Author.DoesNotExist, e:
                author = Author()
                author.firstname = " ".join(gauthor.split(" ")[:-1]).strip()
                author.lastname = gauthor.split(" ")[-1]
                author.save()

            self.authors.add(author)

        for identifier in gbook.identifier:
            id = identifier.text
            if id.startswith("ISBN:"):
                isbn = id.replace("ISBN:", "")
                if len(isbn) == 13 and self.isbn13 == "":
                    self.isbn13 = isbn
                elif len(isbn) == 10 and self.isbn10 == "":
                    self.isbn10 = isbn
            else:
                if self.gid == "":
                    self.gid = id


        if self.cover is None or self.cover == "":
            headers = {'User-Agent': settings.DEFAULT_HTTP_HEADERS}
            f = NamedTemporaryFile(delete=False)
            f.write(urllib2.urlopen(urllib2.Request(cover_link, headers=headers)).read())
            f.filename = f.name
            f.close()

            self.cover.save(
                "temp_filename.jpg",
                File(open(f.name))
            )

            os.unlink(f.name)

    def save(self, cache_book_info=False):
        if self.gid != "" and cache_book_info:
            self.cache_book_info(self.gid)

        if self.slug == "":
            self.slug = slugify(self.title)

        if self.key == "":
            salt = sha(str(random.random())).hexdigest()[:5]
            self.key = sha(salt+self.title).hexdigest()[:30]

        if len(Format.objects.filter(ebook=self)) > 0:
            self.is_ebook = True
        else:
            self.is_ebook = False

        super(Book, self).save()

class Format(models.Model):
    ebook = models.ForeignKey(Book, db_index=True)
    format = models.CharField(choices=FORMAT_CHOICES, max_length=20)
    ebook_file = models.FileField(upload_to=book_save)

    class Meta:
        unique_together = (('ebook', 'format'),)

    def __str__(self):
        return "%s" % (self.format)

class Category(models.Model):
    name = models.CharField(max_length=20)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return "%s" % (self.name)

class Author(models.Model):
    firstname = models.CharField(max_length=50, db_index=True)
    lastname = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)

class CheckOut(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    book = models.ForeignKey(Book, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.user.username)
