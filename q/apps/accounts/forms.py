from django import forms
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.models import User

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
    
    def clean_username(self):
        username = self.cleaned_data['username']
        #try:
        #    user = User.objects.get(username=username)
        #except User.DoesNotExist:
        #    return username

        raise forms.ValidationError(u'Username "%s" already exists.' % username )


    
    
class InvitationDistributionForm(forms.Form):
	
	number_of_invites = forms.IntegerField(label=_('Number of Invites'),)
	to_who = forms.ChoiceField(label=_('To'))
    

	def __init__(self, *args, **kwargs):
		if kwargs.has_key('users'):
			users = kwargs.pop('users')
		else:
			users =(None, None)

		super(InvitationDistributionForm, self).__init__(*args, **kwargs)

		self.fields['to_who'].choices = [(u.id, u.username) for u in users]
