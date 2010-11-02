from django.contrib import admin
from q.ebooks import models

class FormatInline(admin.TabularInline):
    model = models.Format
    extra = 5

class BookAdmin(admin.ModelAdmin):
    exclude = ['authors',]
    list_display = ['title', 'gid',]
    search_fields = ['title', 'isbn10']#, 'authors__firstname', 'authors__lastname']
    inlines = [
        FormatInline,
    ]

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        if instance.gid != "":
            instance.cache_book_info()
        instance.save()
        return instance

class FormatAdmin(admin.ModelAdmin):
    search_fields = ['ebook__title', 'ebook__isbn10',]
            #'ebook__authors__firstname', 'ebook__authors__lastname', 'ebook__categories']

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['firstname', 'lastname']

class CategoryAdmin(admin.ModelAdmin):
    pass

class CheckOutAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'create_time']

class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'book']

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()

        instance.book.is_physical = True
        instance.book.save()

        return instance


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Format, FormatAdmin)
admin.site.register(models.Author, AuthorAdmin)

admin.site.register(models.CheckOut, CheckOutAdmin)
admin.site.register(models.Ownership, OwnershipAdmin)

