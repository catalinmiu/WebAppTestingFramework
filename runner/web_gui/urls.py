from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('project/<int:project_id>/', views.project, name="project"),
    path('runnedtests', views.runnedTests, name="runnedtests"),
    path('runnedtest/<int:runnedtest_id>/', views.runnedTest, name="runnedtest"),
    path('raport/<int:raport_id>/', views.raport, name="raport"),
]
