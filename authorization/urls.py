from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('activate/', views.create_account),
    path('login/', views.sign_in),
    path('forgot/', views.forgot_password),
    path('logout/', views.logout_user),

    # redirect everything else to login
    path('', lambda _: redirect('/login/')),
]
