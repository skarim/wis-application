from django.urls import path, re_path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('signup/', views.create_account, name='create_account'),
    path('reset/', views.reset_password, name='reset_password'),
    path('login/', views.sign_in, name='sign_in'),
    path('forgot/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_user, name='logout_user'),

    # redirect everything else to login
    re_path(r'', lambda _: redirect('sign_in')),
]
