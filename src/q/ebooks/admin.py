from django.contrib import admin
from q.ebooks import models

class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'isbn', 'author']

class FormatAdmin(admin.ModelAdmin):
    search_fields = ['ebook__title', 'ebook__isbn',
            'ebook__author']

admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Format, FormatAdmin)
