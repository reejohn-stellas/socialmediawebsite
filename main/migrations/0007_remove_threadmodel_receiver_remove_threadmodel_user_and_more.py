# Generated by Django 4.1 on 2022-08-20 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_threadmodel_messagemodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='threadmodel',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='threadmodel',
            name='user',
        ),
        migrations.DeleteModel(
            name='MessageModel',
        ),
        migrations.DeleteModel(
            name='ThreadModel',
        ),
    ]
