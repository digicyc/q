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
    
class InvitationKeyForm(forms.Form):
	name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	
class RegistrationForm(forms.Form):
    name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    kindle_email = forms.EmailField(required=False)