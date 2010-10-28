from django.contrib import admin
from q.accounts import models

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.UserProfile, UserProfileAdmin)
