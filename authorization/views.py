from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseNotAllowed
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from mongoengine import ValidationError, DoesNotExist, MultipleObjectsReturned

from application.models import *
from application.settings import DEBUG


def sign_in(request):
    state, next_page = ('',)*2
    if request.method == 'POST':
        try:
            user = VolunteerUser.objects.get(email=request.POST['username'])
            if user.check_password(request.POST['password']):
                if user.company:
                    user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST['next'])
                    return redirect('dashboard.views.home')
                else:
                    state = ("User has an inactive account. Please contact "
                             "support@eventable.com to reactivate.")
            else:
                state = "Incorrect username/password combination"
        except DoesNotExist:
            state = "User does not exist"
    elif 'next' in request.GET:
        next_page = request.GET['next']
    params = {'state': state, 'next': next_page}
    return render_to_response(
        'login.html', params,
        context_instance=RequestContext(request)
    )


def logout_user(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('authorization.views.sign_in')