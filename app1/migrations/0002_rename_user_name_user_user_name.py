# Generated by Django 4.1.2 on 2022-10-18 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='User_Name',
            new_name='user_Name',
        ),
    ]
