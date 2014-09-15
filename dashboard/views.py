from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from mongoengine import ValidationError, DoesNotExist, MultipleObjectsReturned

from application.models import *
from application.settings import DEBUG


@login_required
def dashboard(request):
    return render_to_response(
        'dashboard.html',
        context_instance=RequestContext(request)
    )