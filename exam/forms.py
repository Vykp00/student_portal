from django import forms
from ckeditor.widgets import CKEditorWidget
from exam.models import Answer, Exams, Question, Answer

# Page Form
class NewExamForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    description = forms.CharField(widget=CKEditorWidget())
    # Allow form to pick and validate the date
    due= forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}), required=True)
    allowed_attempts = forms.IntegerField(max_value=100, min_value=1)
    time_limit_mins = forms.IntegerField(max_value=360, min_value=10)

    class Meta:
        model = Exams
        fields = ('title', 'description', 'due', 'allowed_attempts', 'time_limit_mins')

class NewQuestionForm(forms.ModelForm):
    question_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    points = forms.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Question
        fields = ('question_text', 'points')

class NewAnswerForm(forms.ModelForm):
    answer_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    is_correct = forms.BooleanField(required=True)

    class Meta:
        model = Answer
        fields = ('answer_text', 'is_correct')

