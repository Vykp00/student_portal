from dataclasses import field, fields
import imp
from pyexpat import model
from django import forms
from module.models import Module

class NewModuleForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    hours = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)

    class Meta:
        model = Module
        fields = {'title', 'hours'}