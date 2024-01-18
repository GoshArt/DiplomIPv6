import json

from django.shortcuts import render, redirect
from django.template.context_processors import static

from main.models import User
from main.models import Test
from main.models import Task
from main.models import TestAnswer
from main.models import TaskAnswer
from main.models import RecordingAddresses
from django.utils.html import escape
import random


def add_data(request):
    full = open("main/static/main/address/full.txt", "r+")
    small = open("main/static/main/address/small.txt", "r+")
    for i in range(150):
        full_line = full.readline()
        small_line = small.readline()
        record_address = RecordingAddresses(full_record=full_line[0:39], abbreviation=small_line[0:39])
        record_address.save()
    return redirect('/')


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
            test_answer = TestAnswer(test_result=calculation_result(len(test.test_answer), result_test), test_id_id=test.id, user_id_id=request.session['id'])
            test_answer.save()
            if int(num) == 1:
                if request.session['result'] > "2":
                    user = User.objects.get(id=request.session['id'])
                    user.theme_status = user.theme_status[:0] + '1' + user.theme_status[1:]
                    user.save(update_fields=["theme_status"])
                return render(request, 'result_task_page.html',
                              {'result': request.session['result'], 'number': num})
            return redirect('/test_result')
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
        status = list(User.objects.get(id=request.session['id']).theme_status)
        return render(request, 'index.html', {'auth': request.session.get('auth'),
                                              'status1': status[0], 'status2': status[1], 'status3': status[2],
                                              'status4': status[3], 'status5': status[4], 'status6': status[5]})


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
    if request.session.get('auth') and request.method == 'POST':
        form = dict(request.POST)
        num = int(form.get('number')[0])
        return render(request, 'tasks/task' + str(num) + '.html', {'auth': request.session.get('auth')})
    else:
        return redirect('/login')


def processing_task_results(request):
    if request.method == 'POST':
        form = dict(request.POST)
        num = int(form.get('number')[0])
        result_task = 0
        if num == 2:
            task = Task.objects.filter(task_number=str(num)).first()
            answers = json.loads(task.task_answer)
            for i in range(8):
                if form.get('formChoice' + str(i + 1))[0] == answers['naming'][i]:
                    result_task += 1
            for i in range(8):
                if form.get('size' + str(i + 1))[0] == answers['len'][i]:
                    result_task += 1
            task_answer = TaskAnswer(task_result=calculation_result(16, result_task), task_id_id=task.id, user_id_id=request.session['id'])
            task_answer.save()
            if calculation_result(16, result_task) > "2":
                user = User.objects.get(id=request.session['id'])
                user.theme_status = user.theme_status[:1] + '1' + user.theme_status[2:]
                user.save(update_fields=["theme_status"])
            return render(request, 'result_task_page.html',
                          {'result': calculation_result(16, result_task), 'number': num})

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
            request.session['role'] = user.role
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


def task3(request):
    return render(request, 'tasks/task3.html', {'auth': request.session.get('auth')})


def task4(request):
    return render(request, 'tasks/task4.html', {'auth': request.session.get('auth')})

def teacher_page(request):
    if request.session.get('auth') and request.session.get('role') == "TEACHER" or request.session.get('role') == "OWNER":
        return render(request, 'teacher_page.html', {'auth': request.session.get('auth')})
    else:
        return redirect('/login')