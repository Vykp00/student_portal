from unicodedata import name
from django.urls import path
from course.views import CategoryView, CategoryCourses, NewCourse, Enroll, DeleteCourse, EditCourse, MyCourses, CourseDetail

from module.views import NewModule, CourseModules
from page.views import NewPageModules, PageDetail
from exam.views import NewExam, NewQuestion, ExamDetail, TakeExam, SubmitAttempt, Result
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

    # Page - Views (since it's connected to exam view it need /pages/)
    path('<course_id>/module/<module_id>/pages/newpage', NewPageModules, name='new-page'),
    path('<course_id>/module/<module_id>/pages/<page_id>', PageDetail, name='page-detail'),

    # Exam - Views
    path('<course_id>/module/<module_id>/exam/newexam', NewExam, name='new-exam'),
    path('<course_id>/module/<module_id>/exam/<exam_id>/newquestion', NewQuestion, name='new-question'),
    path('<course_id>/module/<module_id>/exam/<exam_id>/', ExamDetail, name='exam-detail'),
    path('<course_id>/module/<module_id>/exam/<exam_id>/take', TakeExam, name='take-exam'),
    path('<course_id>/module/<module_id>/exam/<exam_id>/take/submit', SubmitAttempt, name='submit-exam'),
    path('<course_id>/module/<module_id>/exam/<exam_id>/<attempt_id>/results', Result, name='result'),
]