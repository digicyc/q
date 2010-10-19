from django.contrib import admin
from q.ebooks import models

class FormatInline(admin.TabularInline):
    model = models.Format
    extra = 5

class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'isbn', 'author__firstname', 'author__lastname']
    inlines = [
        FormatInline,
    ]

class FormatAdmin(admin.ModelAdmin):
    search_fields = ['ebook__title', 'ebook__isbn',
            'ebook__author__firstname', 'ebook__author__lastname']
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['firstname', 'lastname']

admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Format, FormatAdmin)
admin.site.register(models.Author, AuthorAdmin)