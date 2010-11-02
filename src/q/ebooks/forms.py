from django import forms

class CheckOutForm(forms.Form):

    to_who = forms.ChoiceField(required=True, label='Checkout To')

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('users'):
            users = kwargs.pop('users')

        super(CheckOutForm, self).__init__(*args, **kwargs)

        self.fields['to_who'].choices = [(u.id, u.username) for u in users]

