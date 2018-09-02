from django.urls import include, path

from . import views

urlpatterns = [
    # admin views
    path('volunteers/', views.admin_manage_volunteers, name='admin_manage_volunteers'),
    path('volunteers/view/', views.admin_view_volunteer, name='admin_view_volunteer'),
    path('dates/', views.admin_manage_dates, name='admin_manage_dates'),
    path('dates/view/', views.admin_view_date, name='admin_view_date'),

    # volunteer views
    path('register/', views.volunteer_register, name='volunteer_register'),
    path('manage/', views.volunteer_manage_registrations, name='volunteer_manage_registrations'),

    path('', views.dashboard, name='dashboard'),
    path('settings/', views.account_settings, name='account_settings'),
]
