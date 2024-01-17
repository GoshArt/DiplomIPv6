import json

from django.shortcuts import render, redirect
from main.models import User
from main.models import Test
from main.models import Task
from main.models import TestAnswer
from main.models import TaskAnswer
from django.utils.html import escape
import random


def calculation_result(total, right):
    res = right / total
    if res <= 0.4:
        return '2'
    elif 0.4 < res <= 0.7:
        return '3'
    elif 0.7 < res <= 0.9:
        return '4'
    else:
        return '5'


def testing(request):
    if request.session.get('auth'):
        form = dict(request.POST)
        num = int(form.get('number')[0])
        if request.method == 'POST':
            result_test = 0
            test = Test.objects.filter(test_number=str(num)).first()
            for i in range(len(form)):
                if form.get('question' + str(i + 1)) is not None:
                    if form.get('question' + str(i + 1))[0] == test.test_answer[i]:
                        result_test += 1
            if len(form) == 2:
                return render(request, 'tests/test' + str(num) + '.html', {'auth': request.session.get('auth')})
            request.session['result'] = calculation_result(len(test.test_answer), result_test)
            request.session['number'] = num
            test_answer = TestAnswer(test_result=result_test, test_id_id=test.id, user_id_id=request.session['id'])
            test_answer.save()
            return redirect('/result')
        else:
            return render(request, 'tests/test' + str(num) + '.html', {'auth': request.session.get('auth')})
    else:
        return redirect('/login')


def index(request):
    if request.session.get('auth') is None:
        return redirect('/registration')
    elif request.session.get('auth') is False:
        return redirect('/login')
    else:
        return render(request, 'index.html', {'auth': request.session.get('auth')})


def result(request):
    if request.session.get('auth'):
        if request.session.get('result'):
            result_test = request.session['result']
            number = request.session['number']
            request.session['result'] = ''
            request.session['number'] = ''
            return render(request, 'result_page.html', {'result': result_test, 'number': number})
        else:
            return redirect('/')
    else:
        return redirect('/login')


def exercise(request):
    if request.session.get('auth'):
        form = dict(request.POST)
        num = int(form.get('number')[0])
        if request.method == 'POST':
            result_task = 0
            task = Task.objects.filter(task_number=str(num)).first()
            answers = json.loads(task.task_answer)
            if num == "2":
                for i in range(8):
                    if form.get('formChoice' + str(i + 1))[0] == answers['naming'][i]:
                        result_task += 1
                for i in range(8):
                    if form.get('size' + str(i + 1))[0] == answers['len'][str(i+1)]:
                        result_task += 1
                print(result_task)
            if len(form) == 2:
                return render(request, 'tasks/task' + str(num) + '.html', {'auth': request.session.get('auth')})
            request.session['result'] = calculation_result(len(task.task_answer), result_task)
            request.session['number'] = num
            task_answer = TaskAnswer(task_result=result_task, task_id_id=task.id, user_id_id=request.session['id'])
            task_answer.save()
            return redirect('/result')
        else:
            return render(request, 'task/task' + str(num) + '.html', {'auth': request.session.get('auth')})
    else:
        return redirect('/login')


def login(request):
    if request.method == 'POST' and request.POST['username'] is not None and request.POST['password'] is not None and \
            not request.session.get('auth'):
        username = escape(request.POST['username'])
        password = escape(request.POST['password'])
        user = User.objects.filter(user_nickname=username, user_password=password).first()
        if user:
            request.session['auth'] = True
            request.session['name'] = username
            request.session['id'] = user.id
            request.session['result'] = ''
            return redirect('/')
    return render(request, 'login.html')


def logout(request):
    request.session['auth'] = False
    request.session['name'] = ''
    request.session['id'] = ''
    return redirect('/')


def registration(request):
    if request.method == 'POST' and request.POST['username'] is not None and request.POST['numberGroup'] is not None and \
            request.POST['codeReg'] is not None and request.POST['password'] is not None and \
            (10 >= len(request.POST['password']) >= 0) and request.POST['codeReg'] == 'test':
        user = User(user_nickname=request.POST['username'],
                    user_password=request.POST['password'],
                    student_group=request.POST['numberGroup'])
        user.save()
        return redirect('/login')
    return render(request, 'registration.html', {'auth': request.session.get('auth')})


def lecture(request):
    if request.session.get('auth'):
        form = dict(request.POST)
        num = int(form.get('number')[0])
        return render(request, 'lectures/lecture' + str(num) + '.html', {'auth': request.session.get('auth')})
    else:
        return redirect('/login')


def task2(request):
    return render(request, 'tasks/task2.html', {'auth': request.session.get('auth')})


def task3(request):
    return render(request, 'tasks/task3.html', {'auth': request.session.get('auth')})


def task4(request):
    return render(request, 'tasks/task4.html', {'auth': request.session.get('auth')})
