# Generated by Django 4.1.2 on 2022-11-30 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_alter_myride_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='myride',
            name='price',
            field=models.IntegerField(default='0'),
        ),
    ]
