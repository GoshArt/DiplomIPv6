from django.db import models
from main.model_choises import *


# Create your models here.
class User(models.Model):
    user_nickname = models.CharField(max_length=50)
    user_password = models.CharField(max_length=12)
    student_group = models.IntegerField()
    role = models.CharField(choices=USER_ROLES.USER_ROLE_CHOISES, default=USER_ROLES.STUDENT)
    theme_status = models.CharField(max_length=10, default="0000000000")
    user_registration_rate = models.DateTimeField(auto_now_add=True)


class Test(models.Model):
    test_number = models.IntegerField()
    test_answer = models.CharField(max_length=400)
    create_date = models.DateTimeField(auto_now_add=True)


class TestAnswer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    test_id = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
    test_result = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    task_number = models.IntegerField()
    task_question = models.CharField(max_length=400)
    task_answer = models.CharField(max_length=400)
    create_date = models.DateTimeField(auto_now_add=True)


class TaskAnswer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    task_id = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    task_result = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
