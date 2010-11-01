from django import forms

class CheckOutFromUser(forms.Form):
    
    owners = forms.ChoiceField(required=True, label='Check Out From')
    
    def __init__(self, *args, **kwargs):
        owners = kwargs.pop('owners')
        super(CheckOutFromUser, self).__init__(*args, **kwargs)
        self.fields['owners'].choices = [(t.user.id, t.user.username) for t in owners]