import imp
from turtle import title
from django.shortcuts import render, get_object_or_404, redirect
from module.forms import NewModuleForm
from module.models import Module
from course.models import Course
from django.http import HttpResponseForbidden

# Create your views here.

def NewModule(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user !=course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewModuleForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                hours = form.cleaned_data.get('hours')
                m = Module.objects.create(title=title, hours=hours, user=user)
                course.modules.add(m)
                course.save()
                return redirect('modules', course_id=course_id)
        else:
            form = NewModuleForm()
    context = {
            'form': form,
    }
    return render(request, 'module/newmodule.html', context)

def CourseModules(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    instructor_mode = False

    if user == course.user:
        instructor_mode = True
    context = {
        'course': course,
        'instructor_mode': instructor_mode,
    }
    return render(request, 'module/modules.html', context)
