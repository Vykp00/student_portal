from distutils.command.upload import upload
from email.policy import default
from statistics import mode
from tabnanny import verbose
from tokenize import Comment
from turtle import title
from django.db import models
from django.contrib.auth.models import User
import os

# 3rd app fields
from ckeditor.fields import RichTextField

# Create your models here.
def user_directory_path(instance, filename):
    # This file will be uploaded to MEDIA_ROOT / the user(id)/the file
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Return file name object in module
class AssignmentFileContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)

    def get_file_name(self):
        return os.path.basename(self.file.name)

class Assignment(models.Model):
    title = models.CharField(max_length=150, default="assignment", null=False, verbose_name='Title')
    content = RichTextField()
    points = models.PositiveIntegerField()
    due = models.DateField()
    files = models.ManyToManyField(AssignmentFileContent)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Submission(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    comment = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_file_name(self):
        return os.path.basename(self.file.name)