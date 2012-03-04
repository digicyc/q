from django import forms

import models

class UserProfile(forms.ModelForm):
    class Meta:
        model = models.UserProfile