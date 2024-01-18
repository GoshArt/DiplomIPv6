from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('testing', views.testing),
    path('test_result', views.result),
    path('logout', views.logout),
    path('login', views.login),
    path('registration', views.registration),
    path('lecture', views.lecture),
    path('testing', views.testing),
    path('exercise', views.exercise),
    path('ex_results', views.processing_task_results),
    path('task3', views.task3),
    path('task4', views.task4),
]
