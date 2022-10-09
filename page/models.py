from enum import auto
import imp
from turtle import title
from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

# 3rd app fields
from ckeditor.fields import RichTextField
def user_directory_path(instance, filename):
    # This file will be uploaded to MEDIA_ROOT / the user(id)/the file
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Return file name object in module
class PostFileContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    posted = models.DateTimeField(auto_now_add=True)

    def get_file_name(self):
        return os.path.basename(self.file.name)

# Page Object for Form
class Page(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextField()
    files = models.ManyToManyField(PostFileContent)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_owner')

    def __str__(self):
        return self.title