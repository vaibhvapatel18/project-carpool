# Generated by Django 4.1.2 on 2022-12-07 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0032_delete_rideinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rideinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_point', models.CharField(max_length=50)),
                ('pickout_point', models.CharField(max_length=50)),
                ('arrival_time', models.CharField(max_length=50)),
                ('drop_time', models.CharField(max_length=50)),
                ('date', models.CharField(max_length=20)),
                ('allowed_participants', models.IntegerField()),
                ('price', models.IntegerField()),
                ('ride_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=12)),
            ],
        ),
    ]
