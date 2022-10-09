import imp
from socket import fromshare
from sys import modules
from django import forms
from page.models import Page
from ckeditor.widgets import CKEditorWidget

# Page Form
class NewPageForm(forms.ModelForm):
    title = forms.ImageField()
    content = forms.CharField(widget=CKEditorWidget())
    # Allow multiple file submission
    files= forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}), required=False)

    class Meta:
        model = Page
        fields = ('title', 'content', 'files')