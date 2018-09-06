from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.core.validators import validate_email
from django.contrib.auth.models import User as DjangoUserClass

from application.models import *
from application.settings import ADMIN_KEY

from services.emails import send_password_reset_email


def create_account(request):
    state = ''
    if request.method == 'POST':
        try:
            # get data from form
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            account_type = request.POST.get('type', 'volunteer')
            nonce = request.POST.get('nonce')

            # basic validations
            if len(password) < 8:
                state = 'Passwords must be at least 8 characters'
            elif password != confirm_password:
                state = 'Passwords do not match'
            elif not first_name or not last_name:
                state = 'Please enter a first and last name'
            else:
                try:
                    validate_email(email)
                except:
                    state = 'Invalid email address'

            if not state:
                if account_type == 'admin':
                    if request.POST.get('admin_key') != ADMIN_KEY:
                        state = 'Invalid admin sign up key'
                    else:
                        # create admin user
                        user = WIS_User(
                            username=email,
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            is_admin=True,
                            is_volunteer=False,
                            is_staff=True,
                            is_superuser=True,
                        )
                else:
                    try:
                        user = WIS_User.objects.get(email=email, is_active=False)
                        if user.nonce and user.nonce != nonce:
                            state = 'Invalid activation link. Please use the password '\
                                    'reset form to get a new link.'
                    except:
                        state = 'Email not registered with WIS. ' \
                                'Please contact the admin for help.'

            if user and not state:
                # if all good, set password and clear out nonce
                user.set_password(password)
                user.is_active = True
                user.nonce = None
                user.save()
                # login and redirect
                login(request, user)
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
        except Exception as e:
            state = 'Error: {0}'.format(e)

    params = {
        'state': state
    }
    return render(
        request,
        'signup.html',
        params,
    )


def sign_in(request):
    # redirect to dashboard is user already logged in
    if request.user:
        try:
            user = WIS_User.objects.get(email=request.user, is_active=True)
            return redirect('dashboard')
        except:
            pass

    state = ''
    if request.method == 'POST':
        try:
            user = WIS_User.objects.get(email=request.POST.get('email'))
            if user.check_password(request.POST.get('password')):
                login(request, user)
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                state = "Incorrect username/password combination"
        except Exception as e:
            print(e)
            state = "User does not exist"
    params = {
        'state': state
    }
    return render(
        request,
        'login.html',
        params,
    )


def forgot_password(request):
    success, error = ('',)*2
    if request.method == 'POST':
        try:
            # get user from db
            user = WIS_User.objects.get(email=request.POST.get('email'))
            # set new nonce
            user.nonce = DjangoUserClass.objects.make_random_password(length=16)
            user.save()
            # send password reset email to user
            send_password_reset_email(user)
            success = "A password reset link has been emailed to you"
        except:
            error = "User does not exist"
    params = {
        'success': success,
        'error': error
    }
    return render(
        request,
        'forgot.html',
        params,
    )


def reset_password(request):
    state = ''
    if request.method == 'POST':
        try:
            user = WIS_User.objects.get(email=request.POST.get('email'))
            nonce = request.POST.get('nonce')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if user.nonce and user.nonce != nonce:
                state = 'Invalid password reset link. Please use the password '\
                        'reset form to get a new link.'
            elif len(password) < 8:
                state = 'Passwords must be at least 8 characters'
            elif password != confirm_password:
                state = 'Passwords do not match'
            else:
                # if all good, reset password and clear out nonce
                user.set_password(password)
                user.nonce = None
                user.save()
                # login and redirect
                login(request, user)
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
        except Exception as e:
            state = "Error: {0}".format(e)
    params = {
        'state': state
    }
    return render(
        request,
        'reset.html',
        params,
    )


def logout_user(request):
    logout(request)
    return redirect('sign_in')
