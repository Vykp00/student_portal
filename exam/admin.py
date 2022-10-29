from django.contrib import admin
from exam.models import Answer, Question, Exams, Learner, Attempt

# Register your models here.
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Exams)
admin.site.register(Learner)
admin.site.register(Attempt)