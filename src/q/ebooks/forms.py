from django import forms
from q.ebooks.models import Book, Format

class CheckOutForm(forms.Form):

    to_who = forms.ChoiceField(required=True, label='Checkout To')

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('users'):
            users = kwargs.pop('users')

        super(CheckOutForm, self).__init__(*args, **kwargs)

        self.fields['to_who'].choices = [(u.id, u.username) for u in users]


class BookForm(forms.Form):
    title = forms.CharField(required=True, label="Title", max_length=100)
    authors = forms.CharField(required=True, label="Author(s)")
    tags = forms.CharField(label="Tags", required=False)
    isbn10 = forms.CharField(max_length=20, label="ISBN10")
    isbn13 = forms.CharField(max_length=20, label="ISBN13")
    gid = forms.CharField(max_length=20, label="Google Id")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    #cover = forms.ImageField(label="Cover", required=False)
    metarating = forms.FloatField(label="metarating", widget=forms.HiddenInput, initial="0.0")

class UploadFormatForm(forms.Form):
    book = forms.FileField(label="")
