# Generated by Django 5.0.1 on 2024-01-18 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_user_theme_status_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordingAddresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_record', models.CharField(max_length=50)),
                ('abbreviation', models.CharField(max_length=50)),
            ],
        ),
    ]
