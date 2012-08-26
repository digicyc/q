from django import forms
from ebooks.models import Book, Format

class CheckOutForm(forms.Form):

    to_who = forms.ChoiceField(label='Checkout To')
    notes = forms.CharField(label="Notes", widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('users'):
            users = kwargs.pop('users')
        else:
            users =(None, None)

        super(CheckOutForm, self).__init__(*args, **kwargs)

        self.fields['to_who'].choices = [(u.id, u.username) for u in users]


class BookForm(forms.Form):
    title = forms.CharField(required=True, label="Title*", max_length=100)
    cover_url = forms.URLField(label="Cover URL*", required=True)
    authors = forms.CharField(required=True, label="Author(s)* [firstname lastname, firstname lastname]")
    series = forms.CharField(max_length=100, label="Series", required=False)
    series_num = forms.IntegerField(label="Series Number", required=False)
    tags = forms.CharField(label="Tags", required=False)
    isbn10 = forms.CharField(max_length=20, label="ISBN10", required=False)
    isbn13 = forms.CharField(max_length=20, label="ISBN13", required=False)
    description = forms.CharField(label="Description*", widget=forms.Textarea, required=True)
    #metarating = forms.FloatField(label="metarating", widget=forms.HiddenInput, initial="0.0")

class UploadFormatForm(forms.Form):
    book = forms.FileField(label="")
