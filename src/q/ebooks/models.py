import os.path

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

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
            instance.ebook.author, extension)
    return os.path.join("books", "files", filename)

def cover_save(instance, original_filename):
    extension = os.path.splitext(original_filename)[1].lower()
    filename = generate_book_filename(instance.title,
            instance.author, extension)
    return os.path.join("books", "covers", filename)

def generate_book_filename(title, author, extension):
    filename = slugify("%s_%s" % (title, author))

    return "%s.%s" % (filename, extension.replace('.', ''))

class Book(models.Model):
    title = models.CharField(db_index=True, max_length=100)
    # m2m in the future
    authors = models.ManyToManyField("Author")
    metarating = models.FloatField()
    rating = models.FloatField()
    #tags = models.ManyToMany("Tags")
    isbn10 = models.CharField(db_index=True, max_length=20, blank=True)
    isbn13 = models.CharField(db_index=True, max_length=20, blank=True)
    gid = models.CharField(db_index=True, max_length=20, blank=True)
    description = models.TextField(blank=True)
    published = models.DateField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to=cover_save, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    is_physical = models.BooleanField(default=False)
    is_ebook = models.BooleanField(default=False)
    checked_out = models.ForeignKey(User, null=True, blank=True)

    def _get_categories(self):
        return Category.objects.filter(books=self)
    categories = property(_get_categories)

    def __str__(self):
        return "%s" % (self.title)

    def _get_formats(self):
        return Format.objects.filter(ebook=self).order_by('format')
    formats = property(_get_formats)

class Format(models.Model):
    ebook = models.ForeignKey(Book)
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
