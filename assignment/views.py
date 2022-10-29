import imp
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from assignment.forms import NewAssignmentForm, NewSubmissionForm
from assignment.models import AssignmentFileContent, Assignment
from module.models import Module

# Create your views here.
def NewAssignment(request, course_id, module_id):
    user = request.user
    module = get_object_or_404(Module, id=module_id)
