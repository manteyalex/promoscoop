from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='contest-home'),
    path('about/', views.about, name='contest-about'),
]