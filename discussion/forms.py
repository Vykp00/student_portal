from dataclasses import fields
from django import forms
from discussion.models import Question, Answer
from ckeditor.widgets import CKEditorWidget

# Question Form
class QuestionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'validate'}), required=True)
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Question
        fields = ('title', 'content')