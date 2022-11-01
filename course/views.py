from contextlib import redirect_stderr
from email.policy import default
from http.client import HTTPResponse
import imp
from multiprocessing import context
from unicodedata import category, name
from urllib import request
from uuid import UUID
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from course.models import Course, Category, Grade
from course.forms import NewCourseForm

# Create your views here.
# Course Listing Views
def listing(request):
    context = {
        'courses': Course.objects.all(),
    }
    return render(request, 'home.html', context)

# Index views
def index(request):
    user = request.user
    courses = Course.objects.all()

    context = {
        'courses': courses
    }
    return render(request, 'index.html', context)

# Category views
def CategoryView(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'course/category.html', context)

# Show course in a category
def CategoryCourses(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    courses = Course.objects.filter(category=category)
    context = {
        'category': category,
        'courses' : courses,
    }
    return render(request, 'course/category-courses.html', context)

# Create new course view
@login_required
def NewCourse(request):
    user = request.user
    if request.method == 'POST':
        form = NewCourseForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            syllabus = form.cleaned_data.get('syllabus')
            image = form.cleaned_data.get('image')
            pub_date = form.cleaned_data.get('pub_date')
            Course.objects.create(name=name, description=description, category=category, syllabus=syllabus, image=image, pub_date=pub_date, user=user)

            return redirect('my-courses')
        
    else:
        form = NewCourseForm()
    context = {
        'form': form
    }

    return render(request, 'course/newcourse.html', context)
def CourseDetail(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    instructor_mode = False

    if user == course.user:
        instructor_mode = True
    context = {
        'course': course,
        'instructor_mode': instructor_mode,
    }
    return render(request, 'course/course.html', context)

# Create enroll view and check if user is login
@login_required
def Enroll(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    course.learners.add(user)
    course.total_enrollment +=1
    course.save()
    return redirect('index')

# Create delete a course view
@login_required
def DeleteCourse(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    # Check if user is the instructor
    if user !=course.user:
        return HttpResponseForbidden()
    else:
        course.delete()
    return redirect('my-courses')

# Create edit a course view
@login_required
def EditCourse(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user !=course.user:
        return HttpResponseForbidden()
    
    else: 
        if request.method == 'POST':
            form = NewCourseForm(request.POST, request.FILES, instance=course)
            # Check if form is valid
            if form.is_valid():
                course.name = form.cleaned_data.get('name')
                course.description = form.cleaned_data.get('description')
                course.category = form.cleaned_data.get('category')
                course.syllabus = form.cleaned_data.get('syllabus')
                course.image = form.cleaned_data.get('image')
                course.pub_date = form.cleaned_data.get('pub_date')
                course.save()
                return redirect('my-courses')
        else:
            
            form = NewCourseForm(instance=course)
    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'course/edit-course.html', context)

# My course view
def MyCourses(request):
    user = request.user
    if user.is_staff:
        courses = Course.objects.filter(user=user)
    else:
        courses = Course.objects.filter(learners=user)
    context = {
        'courses': courses
    }

    return render(request, 'course/my-courses.html', context)

# Get my submission view from submission app
def Submissions(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    grades = Grade.objects.filter(course=course, submission__user=user)
    context = {
        'grades': grades,
        'course': course,
    }
    return render(request, 'course/submissions.html', context)

# Get student's submission view
def StudentSubmissions(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    if user !=course.user:
        return HttpResponseForbidden()
    else:
        grades = Grade.objects.filter(course=course)
        context = {
        'course': course,
        'grades': grades,
        }
        return render(request, 'course/student-grades.html', context)

# Post grade for submitted assignment view
def GradeSubmission(request, course_id, grade_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    grade = get_object_or_404(Grade, id=grade_id)

    if user !=course.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            points = request.POST.get('points')
            grade.points = points
            grade.status = 'graded'
            grade.graded_by = user
            grade.save()
            
            return redirect('student-submissions', course_id=course_id)

    context = {
        'course': course,
        'grade': grade,
    }
    return render(request, 'course/grade-submission.html', context)
