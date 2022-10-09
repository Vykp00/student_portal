from unicodedata import name
from django.urls import path
from course.views import CategoryView, CategoryCourses, NewCourse, Enroll, DeleteCourse, EditCourse, MyCourses, CourseDetail

from module.views import NewModule, CourseModules
from page.views import NewPageModules, PageDetail
urlpatterns = [
    # Course - Views
    path('newcourse/', NewCourse, name="newcourse"),
    path('mycourses/', MyCourses, name='my-courses'),
    path('category/', CategoryView , name='category'),
    path('category/<category_slug>', CategoryCourses, name='category-courses'),
    path('<course_id>', CourseDetail, name='course'),
    path('<course_id>/enroll', Enroll, name='enroll'),
    path('<course_id>/edit', EditCourse, name='edit-course'),
    path('<course_id>/delete', DeleteCourse, name='delete-course'),

    # Modules - Views
    path('<course_id>/modules', CourseModules, name='modules'),
    path('<course_id>/modules/newmodule', NewModule, name='new-module'),

    # Page - Views
    path('<course_id>/module/<module_id>/newpage', NewPageModules, name='new-page'),
    path('<course_id>/module/<module_id>/<page_id>', PageDetail, name='page-detail'),
]