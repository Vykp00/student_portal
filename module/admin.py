from django.contrib import admin
from module.models import Module

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'hours')

# Register your models here.
admin.site.register(Module)