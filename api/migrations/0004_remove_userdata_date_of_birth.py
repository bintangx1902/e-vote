# Generated by Django 3.2.19 on 2023-12-11 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20231203_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='date_of_birth',
        ),
    ]
