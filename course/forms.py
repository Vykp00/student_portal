from dataclasses import field
from email.mime import image
from importlib.metadata import requires
from pyexpat import model
from socket import fromshare
from tkinter.tix import Form
from tokenize import Triple
from typing_extensions import Required
from unicodedata import category, name
from django import forms
from ckeditor.widgets import CKEditorWidget

from course.models import Category, Course
# Here you create new course
class NewCourseForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    syllabus = forms.CharField(widget=CKEditorWidget())
    image = forms.ImageField(required=True)
    pub_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'validate'}))

    class Meta:
        model = Course
        fields = ('name', 'description', 'category', 'syllabus', 'image', 'pub_date')