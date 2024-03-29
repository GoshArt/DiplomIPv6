# Generated by Django 5.0.1 on 2024-01-14 21:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_number', models.IntegerField()),
                ('task_question', models.CharField(max_length=400)),
                ('task_answer', models.CharField(max_length=400)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_number', models.IntegerField()),
                ('test_answer', models.CharField(max_length=400)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_nickname', models.CharField(max_length=50)),
                ('user_password', models.CharField(max_length=12)),
                ('student_group', models.IntegerField()),
                ('user_registration_rate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_result', models.IntegerField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.test')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.user')),
            ],
        ),
        migrations.CreateModel(
            name='TaskAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_result', models.IntegerField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.task')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.user')),
            ],
        ),
    ]
