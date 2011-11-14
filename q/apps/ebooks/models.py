import os
import os.path
from hashlib import sha256 as sha

import tagging
from tagging.fields import TagField
from djangoratings.fields import RatingField

from django.conf import settings
from django.db import models, connection, transaction
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files import File

from q.common import similarity

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
    checked_out = models.ForeignKey("CheckOut", related_name="checkout_to", null=True, blank=True)
    key = models.CharField(max_length=30, blank=True, db_index=True)

    def __str__(self):
        return "%s's copy of %s" % (self.user, self.book)

    class Meta:
        unique_together = (("user", "book"),)

    def _get_qr_url(self):
            current_site = Site.objects.get_current()
            img_size = "140x140"
            url = "http://chart.apis.google.com/chart?chs="+img_size+"&cht=qr&chl="
            url += current_site.name+"/books/checkout/"+self.key
            url += "&choe=UTF-8"

            return url
    qr_url = property(_get_qr_url)

    def save(self, *args, **kwargs):
        if self.key == "":
            self.key = sha(self.user.username+self.book.title).hexdigest()[:30]
        super(Ownership, self).save()

class Series(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    slug = models.SlugField(max_length=100, blank=True, db_index=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.name)

        super(Series, self).save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(db_index=True, max_length=100)
    authors = models.ManyToManyField("Author", blank=True)
    metarating = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    #tags = TagField()
    isbn10 = models.CharField(db_index=True, max_length=20, blank=True)
    isbn13 = models.CharField(db_index=True, max_length=20, blank=True)
    gid = models.CharField(db_index=True, max_length=20, blank=True)
    description = models.TextField(blank=True)
    published = models.DateField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to=cover_save, blank=True)
    thumbnail = models.ImageField(upload_to=thumb_save, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True)
    series = models.ForeignKey(Series, blank=True, null=True, default=None)
    series_num = models.IntegerField(blank=True, null=True, default=None)

    def _get_is_physical(self):
        if len(self.owners) > 0:
            return True
        return False
    is_physical = property(_get_is_physical)

    def _get_is_ebook(self):
        if len(self.formats) > 0:
            return True
        return False
    is_ebook = property(_get_is_ebook)

    def _get_owners(self):
        ownerships = Ownership.objects.filter(book=self)
        owners = [user for user in ownerships]
        return owners
    owners = property(_get_owners)

    def _get_categories(self):
        return Category.objects.filter(books=self)
    categories = property(_get_categories)

    def __str__(self):
        return "%s" % self.title

    def __unicode__(self):
        return self.title.encode('utf8')

    def _get_formats(self):
        return Format.objects.filter(ebook=self).order_by('format')
    formats = property(_get_formats)

    def _has_mobi(self):
        return bool(Format.objects.filter(ebook=self).filter(format='mobi').count())
    has_mobi = property(_has_mobi)

    def also_downloaded(self):
        """
        Return the best matches for a book based on other downloads
        """
        sql = """SELECT asis.object_id, count(distinct asi.actor_id) as downloaded
                    FROM activity_stream_activitystreamitem asi
                        JOIN activity_stream_activitystreamitemsubject asis ON asis.activity_stream_item_id=asi.id
                    WHERE asi.actor_id IN
                        (SELECT DISTINCT asi.actor_id
                            FROM activity_stream_activitystreamitem asi
                                JOIN activity_stream_activitystreamitemsubject asis ON asis.activity_stream_item_id=asi.id
                            WHERE (asi.type_id=5 OR asi.type_id=8)
                                AND asis.content_type_id=11
                                AND asis.object_id=%s)
                        AND (asi.type_id=5 OR asi.type_id=8)
                        AND asis.content_type_id=11
                        AND asis.object_id <> %s
                    GROUP BY asis.object_id
                    ORDER BY downloaded DESC
                    LIMIT 5""" % (self.id, self.id)
        cursor = connection.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()
        books = []
        for row in rows:
            books.append(Book.objects.get(id=row[0]))
        return books

    def cache_book_info(self, gid=None, save_cover=True):
        import urllib2
        from tempfile import NamedTemporaryFile

        from gdata.books import Book as GBook

        if gid is None:
            gid = self.gid

        if gid is None:
            return

        volume_xml = urllib2.urlopen("http://www.google.com/books/feeds/volumes/%s" % gid).read()
        gbook = GBook.FromString(volume_xml)

        #thumbnail_link = gbook.GetThumbnailLink().href
        cover_link = ""
        try:
            cover_link = gbook.GetThumbnailLink().href.replace('zoom=5','zoom=1')
            self.temp_cover_url = cover_link
        except AttributeError, e:
            pass
        
        if self.title == "":
            self.title = gbook.title.text

        if gbook.rating is not None:
            self.metarating = gbook.rating.average

        if gbook.description is not None and self.description == "":
            self.description = gbook.description.text
        self.published_year = gbook.date.text

        self._authors = []
        for gauthor in gbook.creator:
            gauthor = gauthor.text
            try:
                author = Author.objects.get(firstname=" ".join(gauthor.split(" ")[:-1]).strip(), lastname=gauthor.split(" ")[-1])
            except Author.DoesNotExist, e:
                author = Author()
                author.firstname = " ".join(gauthor.split(" ")[:-1]).strip()
                author.lastname = gauthor.split(" ")[-1]
                author.save()


            self._authors.append(gauthor)
            if self.id is not None:
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


        if cover_link and self.cover is None or self.cover == "" and save_cover:
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

    def save(self, *args, **kwargs):
        cache_book_info=False
        if kwargs.has_key('cache_book_info'):
            cache_book_info = bool(kwargs['cache_book_info'])
        if self.gid != "" and cache_book_info:
            self.cache_book_info(self.gid)

        if self.slug == "":
            self.slug = slugify(self.title)

        super(Book, self).save()
tagging.register(Book)

class Format(models.Model):
    ebook = models.ForeignKey(Book, db_index=True)
    format = models.CharField(choices=FORMAT_CHOICES, max_length=20)
    ebook_file = models.FileField(upload_to=book_save)
    uploaded_by = models.ForeignKey(User)
    verified = models.BooleanField(default=False)

    class Meta:
        unique_together = (('ebook', 'format'),)

    def __str__(self):
        return "%s" % self.format

    def download_key(self):
        import base64
        return base64.b64encode('%s::%s::%s'% (self.ebook_file.url, self.ebook.pk, self.format))

class Category(models.Model):
    name = models.CharField(max_length=20)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return "%s" % self.name

class Author(models.Model):
    firstname = models.CharField(max_length=50, db_index=True)
    lastname = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)

    def __unicode__(self):
        return unicode(self.__str__())

class CheckOut(models.Model):
    user = models.ForeignKey(User, null=True)
    book = models.ForeignKey(Ownership, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    check_in_time = models.DateTimeField(default=None, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (("user", "book"))

    def __str__(self):
        return "%s" % self.user.username

class Read(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    rating = RatingField(range=5, can_change_vote=True)
    date_read = models.DateField(default='1970-01-01')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "book"))

#SOUTH RULES
from south.modelsinspector import add_introspection_rules
rules = [
        (
            (TagField, ),
            [],
            {
                "blank": ["blank", {"default": True}],
                "max_length": ["max_length", {"default": 255}],
            },
        ),
    ]

add_introspection_rules(rules, ["^tagging\.fields",])
