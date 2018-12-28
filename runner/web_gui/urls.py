from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('project/<int:project_id>/', views.project, name="project"),
]
