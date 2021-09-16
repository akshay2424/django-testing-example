
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('users', views.user_list, name='user_list'),
    path('demo/', views.DemoView.as_view(), name='demo'),
    path('get_personal_info/', views.PersonalInfoView.as_view(), name='get_personal_info'),
]

