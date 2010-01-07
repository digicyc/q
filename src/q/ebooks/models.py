from django.db import models

FORMAT_CHOICES = (
    ('pdf', 'pdf'),
    ('lit', 'lit'),
    ('mobi', 'mobi'),
)

class Book(models.Model):
    title = models.CharField(db_index=True, max_length=100)
    # m2m in the future
    author = models.CharField(db_index=True, max_length=100)
    #rating = models.IntegerField()
    #tags = models.ManyToMany("Tags")
    isbn = models.CharField(db_index=True, max_length=30)
    published = models.DateField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to="books/covers/")

    def __str__(self):
        return "%s - %s" % (self.title, self.author)

class Format(models.Model):
    ebook = models.ForeignKey(Book)
    format = models.CharField(choices=FORMAT_CHOICES, max_length=20)
    ebook_file = models.FileField(upload_to="ebooks/")

    def __str__(self):
        return "%s - %s (%s)" % (self.ebook.title, self.ebook.author,
                self.format)
