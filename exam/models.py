from email.policy import default
from enum import auto
from multiprocessing.connection import answer_challenge
from tracemalloc import get_object_traceback
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
# Answer model
class Answer(models.Model):
    answer_text = models.CharField(max_length=900)
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text

# Question model
class Question(models.Model):
    question_text = models.CharField(max_length=900)
    answers = models.ManyToManyField(Answer)
    points = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
# Exam model
class Exams(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    due = models.DateField()
    allowed_attempts = models.PositiveIntegerField()
    time_limit_mins = models.PositiveIntegerField()
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title

# Learner model
class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    completed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# Get number of attempt objects
class Attempt(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    # One Learner has many attempt
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete= models.CASCADE)

    # Save the attempt results to get score and show on result page
    def __str__(self):
        return self.learner.user.username + ' - ' + self.answer.answer_text

