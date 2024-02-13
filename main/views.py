import ipaddress
import json

from django.shortcuts import render, redirect

from main.models import User
from main.models import Test
from main.models import Task
from main.models import TestAnswer
from main.models import TaskAnswer
from main.models import RecordingAddresses
from main.models import access_codes
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
    if request.POST.get('number') is None:
        return redirect('/')
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
            test_answer = TestAnswer(test_result=calculation_result(len(test.test_answer), result_test),
                                     test_id_id=test.id, user_id_id=request.session['id'])
            test_answer.save()
            if num == 1 or num == 6:
                if request.session['result'] > "2":
                    user = User.objects.get(id=request.session['id'])
                    user.theme_status = user.theme_status[:num - 1] + '1' + user.theme_status[num:]
                    user.save(update_fields=["theme_status"])
                return render(request, 'result_task_page.html',
                              {'result': request.session['result'], 'number': num})
            return redirect('/test_result')
        else:
            return render(request, 'tests/test' + str(num) + '.html', {'auth': request.session.get('auth')})
    else:
        return redirect('/login')


def index(request):
    if User.objects.filter(role="TEACHER").first() is None:
        full = open("main/static/main/address/full.txt", "r+")
        small = open("main/static/main/address/small.txt", "r+")
        tasks_ans = open("main/static/main/address/task_answer.txt", "r+")
        tests_ans = open("main/static/main/address/test_answer.txt", "r+")
        for i in range(4):
            task_line = tasks_ans.readline()
            Task(task_number=task_line[:1], task_answer=task_line[1:]).save()
        for i in range(5):
            test_line = tests_ans.readline()
            Test(test_number=test_line[:1], test_answer=test_line[1:]).save()
        for i in range(150):
            full_line = full.readline()
            small_line = small.readline()
            RecordingAddresses(full_record=full_line[:39], abbreviation=small_line[:39]).save()
        user = User(user_nickname="admin",
                    user_password="admin",
                    student_group=0,
                    role="TEACHER")
        user.save()
    if request.session.get('auth') is None:
        return redirect('/registration')
    elif request.session.get('auth') is False:
        return redirect('/login')
    else:
        status = list(User.objects.get(id=request.session['id']).theme_status)
        lectures_name = ["Преимущества IPv6", "Заголовок пакета", "Сокращение адресов IPv6",
                         "Создание подсетей в протоколе IPv6", "Специальные адреса IPv6", "Взаимодействие IPv4 и IPv6"]
        data = []
        for i in range(len(lectures_name)):
            if i != 4:  # Убирает 5 недоделанную тему
                data.append({'lecture_name': lectures_name[i], 'status': status[i], 'value': i + 1})
        return render(request, 'index.html',
                      {'auth': request.session.get('auth'), 'role': request.session.get('role'), 'lectures': data})


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
    if request.POST.get('number') is None:
        return redirect('/')
    if request.session.get('auth') and request.method == 'POST':
        form = dict(request.POST)
        num = int(form.get('number')[0])
        if num == 3:
            addresses = RecordingAddresses.objects.order_by('?')[:12]
            id_addresses = []
            f_addresses = []
            a_addresses = []
            i = 0
            for address in addresses:
                id_addresses.append(address.id)
                if i < len(addresses) / 2:
                    f_addresses.append(address.full_record)
                else:
                    a_addresses.append(address.abbreviation)
                i += 1
            request.session["id_addresses"] = id_addresses
            return render(request, 'tasks/task3.html',
                          {'auth': request.session.get('auth'), "f_addresses": f_addresses, "a_addresses": a_addresses})
        if num == 4:
            task_4_data = []
            task_texts = []
            for i in range(3):
                type_task = random.choice([True, False])  # True - 4 бита False - 5 битов
                if type_task:
                    type_task_text = "подсети "
                else:
                    type_task_text = "интерфейса "
                addresses_names = ['a136', 'b062', '7f8c', '974c', 'ff0d', 'cb8b', '8e51', 'afbc',
                                   '11ae', '153f', 'a39f', 'fc97', '0445', '1d4c', '6209', 'ab7a',
                                   '5dc3', '9692', 'd4f1', 'af91', '3c97', '4a0f', '5b60', 'b72b',
                                   'ed0c', '149c', '15dc', '1e69', '687d', 'ba80', '99b9', 'cc8a',
                                   '6358', 'f32e', 'aa29', '4c49', 'b88d', '970e', '3a78', 'f88c',
                                   'b89c', 'da45', '73b6', '180a', '9df3', '85e6', '7f34', '1608',
                                   'd8dd', '719c', '5138', '3f2c', 'a6e8', '22a9', '4eed', '2993',
                                   'f3f8', '5710', '4acc', '2a75', '50a6', '7d28', '8a33', 'fe9a',
                                   'e424', '7d97', '252b', '89f7', '5bd6', '1e4a', '734d', '6bd3',
                                   '1870', 'a633', 'b6b4', '15bf', '7494', '0c7d', '8d98', '2def',
                                   '0ee5', '378b', '8f7d', '6835', 'b0c1', 'f451', 'cc42', '2f39',
                                   '8d51', 'b269', '9729', 'eedc', 'ee80', 'bc4b', 'ce67', 'af69',
                                   '0054', '2329', '7361', '4cbb', 'c368', '7f27', 'a042', 'c5d0',
                                   '3057', 'ee51', 'f62c', '6b13', '1fd0', 'ca8a', '1d23', '3e33',
                                   '1030', '7d04', '61de', '3ae1', '960b', '229f', 'caab', '0000',
                                   'ca32', 'f177', '09f1', '5242', '2883', 'ca35', '2df6', 'bd86']
                random.shuffle(addresses_names)
                address_name = addresses_names[0] + ':' + addresses_names[1] + ':' + addresses_names[1]
                number_of_subnets = random.randint(17, 4080)
                task_text = "Произведите разбиение сети " + address_name + ":: на подсети с использованием идентификатора " + type_task_text + "и укажите " + str(
                    number_of_subnets) + " подсеть."
                task_texts.append(task_text)
                task_4_data.append([type_task, address_name, number_of_subnets])
            request.session["task_4_data"] = task_4_data
            return render(request, 'tasks/task4.html',
                          {'auth': request.session.get('auth'), "tasks": task_texts})
        return render(request, 'tasks/task' + str(num) + '.html', {'auth': request.session.get('auth')})
    else:
        return redirect('/login')


def processing_task_results(request):
    if request.POST.get('number') is None:
        return redirect('/')
    if request.method == 'POST':
        form = dict(request.POST)
        num = int(form.get('number')[0])
        result_task = 0
        grade = 0
        if num == 2:
            task = Task.objects.filter(task_number=str(num)).first()
            answers = json.loads(task.task_answer)
            for i in range(8):
                if str(form.get('formChoice' + str(i + 1))[0]) == str(answers['naming'][i]):
                    result_task += 1
                if str(form.get('size' + str(i + 1))[0]) == str(answers['len'][i]):
                    result_task += 1
            grade = calculation_result(16, result_task)
        if num == 3:
            for i in range(12):
                address = RecordingAddresses.objects.filter(id=request.session["id_addresses"][i]).first()
                if i < 6 and str.strip(form['address'][i].lower()) == str.strip(address.abbreviation):
                    result_task += 1
                if i >= 6 and str.strip(form['address'][i].lower()) == str.strip(address.full_record):
                    result_task += 1
            grade = calculation_result(12, result_task)
        if num == 4:
            i = 0
            for task_data in request.session["task_4_data"]:
                number_of_subnets_hex = hex(int(task_data[2]))[2:]  # True - 4 бита False - 5 битов
                subnet = ":0000:0"
                len_num_sub = len(number_of_subnets_hex)
                if task_data[0]:
                    subnet = subnet[:len(subnet) - len_num_sub - 2] + str(number_of_subnets_hex) + ":0"
                else:
                    subnet = (subnet[:len(subnet) - len_num_sub - 1] +
                              str(number_of_subnets_hex[:len_num_sub - 1]) +
                              ":" + number_of_subnets_hex[len_num_sub - 1:len_num_sub])
                ans_address = task_data[1] + subnet + "000:0000:0000:0000"
                try:
                    if ipaddress.IPv6Address(ans_address) == ipaddress.IPv6Address(form.get('address')[i]):
                        result_task += 1
                except:
                    print("Nop")
                i += 1
            grade = 2 + result_task
        task_answer = TaskAnswer(task_result=grade, task_id_id=Task.objects.filter(task_number=num).first().id,
                                 user_id_id=request.session['id'])
        task_answer.save()
        if grade > "2":
            user = User.objects.get(id=request.session['id'])
            user.theme_status = user.theme_status[:num - 1] + '1' + user.theme_status[num:]
            user.save(update_fields=["theme_status"])
        return render(request, 'result_task_page.html',
                      {'result': grade, 'number': num})
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
    request.session['role'] = ''
    return redirect('/')


def registration(request):
    try:
        code = access_codes.objects.values('access_code').last()['access_code']
    except:
        code = "Сгенерируйте"
    if request.method == 'POST' and request.POST['username'] is not None and request.POST['numberGroup'] is not None and \
            request.POST['codeReg'] is not None and request.POST['password'] is not None and \
            (10 >= len(request.POST['password']) >= 0) and request.POST['codeReg'] == code:
        user = User(user_nickname=request.POST['username'],
                    user_password=request.POST['password'],
                    student_group=request.POST['numberGroup'])
        user.save()
        return redirect('/login')
    return render(request, 'registration.html', {'auth': request.session.get('auth')})


def lecture(request):
    if request.POST.get('number') is None:
        return redirect('/')
    if request.session.get('auth'):
        form = dict(request.POST)
        num = int(form.get('number')[0])
        return render(request, 'lectures/lecture' + str(num) + '.html', {'auth': request.session.get('auth')})
    else:
        return redirect('/login')


def teacher_page(request):
    if request.session.get('auth') and request.session.get('role') == "TEACHER" or request.session.get(
            'role') == "OWNER":
        users = list(User.objects.filter(role="STUDENT").all().order_by('student_group').values('id', 'user_nickname',
                                                                                                'student_group',
                                                                                                'theme_status'))
        counter = 1
        name_themes = ['theme1', 'theme2', 'theme3', 'theme4', 'theme5']
        for user in users:
            ratings = []
            for i in range(5):
                if i == 4:
                    i += 1
                try:
                    test_rating = str(TestAnswer.objects.filter(user_id_id=user['id'], test_id_id=
                    Test.objects.filter(test_number=i + 1).values('id').first()['id']).values(
                        'test_result').last()['test_result'])
                except:
                    test_rating = "-"
                task_rating = ''
                if 0 < i < 4:
                    try:
                        task_rating = '/' + str(TaskAnswer.objects.filter(user_id_id=user['id'], task_id_id=
                        Task.objects.filter(task_number=i + 1).values('id').first()['id']).values(
                            'task_result').last()['task_result'])
                    except:
                        task_rating = '/-'
                ratings.append(test_rating + task_rating)
            themes = dict(zip(name_themes, ratings))
            user.update(themes)
            user.update({'counter': counter})
            counter += 1
        try:
            code = access_codes.objects.values('access_code').last()['access_code']
        except:
            code = "Сгенерируйте"
        return render(request, 'teacher_page.html',
                      {'auth': request.session.get('auth'), 'users': users, 'admin_id': request.session['id'],
                       'code': code})
    else:
        return redirect('/login')


def delete_user(request):
    if request.session.get('auth') and request.session.get('role') == "TEACHER" or request.session.get(
            'role') == "OWNER" and request.POST.get('number') is not None:
        TestAnswer.objects.filter(id=request.POST.get('number')).all().delete()
        TaskAnswer.objects.filter(id=request.POST.get('number')).all().delete()
        User.objects.filter(id=request.POST.get('number')).delete()
        return redirect('/teacher')
    return redirect('/')


def delete_all(request):
    if request.session.get('auth') and request.session.get('role') == "TEACHER" or request.session.get(
            'role') == "OWNER":
        TestAnswer.objects.all().delete()
        TaskAnswer.objects.all().delete()
        User.objects.filter(role="STUDENT").delete()
        return redirect('/teacher')
    return redirect('/')


def replace_pass(request):
    print(request.POST)
    if request.session.get('auth') and (request.session.get('role') == "TEACHER"
                                        or request.session.get('role') == "OWNER") and \
            request.POST.get('oldPassword') is not None and request.POST.get('newPassword') is not None and \
            request.POST.get('repeatPassword') is not None:
        user = User.objects.filter(id=request.session['id']).first()
        print(user)
        if user.user_password == request.POST.get('oldPassword') and request.POST.get(
                'newPassword') == request.POST.get('repeatPassword'):
            user.user_password = request.POST.get('newPassword')
            user.save(update_fields=["user_password"])
            return redirect('/teacher')
        return render(request, 'replace_password.html')
    elif request.session.get('auth') and (request.session.get('role') == "TEACHER" or request.session.get(
            'role') == "OWNER"):
        return render(request, 'replace_password.html')
    return redirect('/')


def generate_code(request):
    dictionary = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    access_code = []
    for _ in range(10):
        access_code.append(dictionary[random.randint(1, len(dictionary) - 1)])
    access_codes(access_code=''.join(access_code)).save()

    return redirect('/teacher')
