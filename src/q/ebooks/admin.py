from django.contrib import admin
from q.ebooks import models

class FormatInline(admin.TabularInline):
    model = models.Format
    extra = 5

class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'isbn10']#, 'authors__firstname', 'authors__lastname']
    inlines = [
        FormatInline,
    ]

class FormatAdmin(admin.ModelAdmin):
    search_fields = ['ebook__title', 'ebook__isbn10',]
            #'ebook__authors__firstname', 'ebook__authors__lastname', 'ebook__categories']

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['firstname', 'lastname']

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Format, FormatAdmin)
admin.site.register(models.Author, AuthorAdmin)
