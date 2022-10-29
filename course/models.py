from email.policy import default
from enum import unique
from random import choices
from secrets import choice
from tabnanny import verbose
import sys
from telnetlib import DO, STATUS
from tkinter import CASCADE
from turtle import mode
from typing_extensions import Required
from unicodedata import category
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from module.models import Module
from assignment.models import Assignment, Submission

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid
from django.urls import reverse


# Create your models here.

# 3rd apps fields
from ckeditor.fields import RichTextField

def user_directory_path(instance, filename):
    # This file will be uploaded to MEDIA_ROOT / the user(id)/the file
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Instructor model
# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username

# Category model
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    icon = models.CharField(max_length=100, verbose_name='Icon', default='lightbulb_outline')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('categories', arg=[self.slug])

    def __str__(self):
        return self.title

# Course Model
class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=False, max_length=100, default='online course', verbose_name='Title')
    image = models.ImageField(upload_to=user_directory_path)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pub_date = models.DateField(null=True)
    syllabus = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructors', default=0)
    total_enrollment = models.IntegerField(default=0)
    learners = models.ManyToManyField(User, related_name='learners')
    modules = models.ManyToManyField(Module)

    def __str__(self):
        return "Title: " + self.name

# Grade model for submission
class Grade(models.Model):
    # Create status_choice for assignment
    NOT_GRADED = 'NG'
    GRADED = 'G'
    STATUS_CHOICES = [
        (NOT_GRADED, 'Not graded'),
        (GRADED, 'Graded'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    # Name of the teacher
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default=NOT_GRADED, max_length=10, verbose_name='Status')
    