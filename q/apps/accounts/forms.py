from django import forms
from django.utils.translation import ugettext_lazy as _ 

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Your Username'))
    password = forms.CharField(label=_('Password'), 
                widget=forms.PasswordInput(), max_length=100) 
                

class EditProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    #username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    kindle_email = forms.EmailField(required=False)


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label=_('Current Password'),
            widget=forms.PasswordInput(), max_length=100)
    new_password1 = forms.CharField(label=_('New Password'),
            widget=forms.PasswordInput(), max_length=100)
    new_password2 = forms.CharField(label=_('Verify Password'),
            widget=forms.PasswordInput(), max_length=100)