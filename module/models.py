from operator import mod
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from page.models import Page
from exam.models import Exams
from assignment.models import Assignment

class Module(models.Model):
    title = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_owner')
    hours = models.PositiveIntegerField()
    pages = models.ManyToManyField(Page)
    exams = models.ManyToManyField(Exams)
    assignment = models.ManyToManyField(Assignment)

    def __str__(self):
        return self.title