from django.conf import settings
from django.template.defaultfilters import slugify

from ebooks import models

if __name__ == "__main__":
    authors = models.Author.objects.all()
    for author in authors:
        try:
            print author
            try:
                author.slug = slugify(author)
                author.save()
            except:
                print author
        except UnicodeEncodeError:
            print author.id