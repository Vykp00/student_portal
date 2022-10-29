from audioop import add
from multiprocessing import context
from pyexpat import model
from turtle import title
from venv import create
from django.shortcuts import render, redirect, get_object_or_404
from urllib import request
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

from exam.forms import NewExamForm, NewQuestionForm
from exam.models import Answer, Question, Exams, Learner, Attempt
from module.models import Module

# Create your views here.
# Create new exam view
# Rememeber to add id to match url path
def NewExam(request, course_id, module_id):
    user = request.user
    module = get_object_or_404(Module, id=module_id )

    if request.method == 'POST':
        form = NewExamForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            due = form.cleaned_data.get('due')
            allowed_attempts = form.cleaned_data.get('allowed_attempts')
            time_limit_mins = form.cleaned_data.get('time_limit_mins')
            exam = Exams.objects.create(user=user, title=title, description=description, due=due, allowed_attempts=allowed_attempts, time_limit_mins=time_limit_mins)
            module.exams.add(exam)
            module.save()
            return redirect('new-question', course_id=course_id, module_id=module_id, exam_id=exam.id)

    else:
        form = NewExamForm()

    context = {
        'form': form,
    }
    return render(request, 'exam/newexam.html', context)

# Create new question view
def NewQuestion(request, course_id, module_id, exam_id):
    user = request.user
    exam = get_object_or_404(Exams, id=exam_id)

    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get('question_text')
            points = form.cleaned_data.get('points')
            # Get answer key and objects key into the question form 
            # QueryDict.getlist(key, default=None) Returns a list of the data with the requested key. Returns an empty list if the key doesn’t exist and default is None.
            #It’s guaranteed to return a list unless the default value provided isn’t a list.
            answer_text = request.POST.getlist('answer_text')
            is_correct = request.POST.getlist('is_correct')
            question = Question.objects.create(question_text=question_text, user=user, points=points)

            # Since answer is many to many fields, need to call zip() function to create tuples of each list based on the no.index (answer , is_correct)
            for a, c in zip(answer_text, is_correct):
                answer = Answer.objects.create(answer_text=a, is_correct=c, user=user)
                question.answers.add(answer)
                question.save()
                exam.questions.add(question)
                exam.save()
            return redirect('new-question', course_id=course_id, module_id=module_id, exam_id=exam.id)
    else:
        form = NewQuestionForm()

    context = {
        'form': form,
    }
    return render(request, 'exam/newquestion.html', context)

# Show exam detail view
def ExamDetail(request, course_id, module_id, exam_id):
    user = request.user
    exam = get_object_or_404(Exams, id=exam_id)
    my_attempts = Learner.objects.filter(exam=exam, user=user)

    context = {
        'exam': exam,
        'my_attempts': my_attempts,
        'course_id': course_id,
        'module_id': module_id,
    }
    return render(request, 'exam/examdetail.html', context)

# Exam views for learner
def TakeExam(request, course_id, module_id, exam_id):
    exam = get_object_or_404(Exams, id=exam_id)
    context = {
        'exam': exam,
        'course_id': course_id,
        'module_id': module_id,
    }
    return render(request, 'exam/takeexam.html', context)

# Get exam submission view
def SubmitAttempt(request, course_id, module_id, exam_id):
    user= request.user
    exam = get_object_or_404(Exams, id=exam_id)
    earned_points = 0
    if request.method == 'POST':
        questions = request.POST.getlist('question')
        answers = request.POST.getlist('answer')
        learner = Learner.objects.create(user=user, exam=exam, score=0)

        # Add question's and submitted answer's id to a tubple with zip function
        for q, a in zip(questions, answers):
            question = Question.objects.get(id=q)
            answer = Answer.objects.get(id=a)
            Attempt.objects.create(exam=exam, learner=learner, question=question, answer=answer)
            
            # Get score
            if answer.is_correct == True:
                earned_points += question.points
                learner.score += earned_points
                learner.save()
        return redirect('index')

# Show result view
def Result(request, course_id, module_id, exam_id, attempt_id):
    user = request.user
    exam = get_object_or_404(Exams, id=exam_id)
    attempts = Attempt.objects.filter(exam=exam, learner__user=user)

    context = {
        'exam': exam,
        'attempts': attempts,
        'course_id': course_id,
        'module_id': module_id,
    }
    return render(request, 'exam/result.html', context)