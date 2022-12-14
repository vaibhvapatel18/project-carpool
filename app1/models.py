from unittest.util import _MAX_LENGTH
from email.policy import default
from django.db import models

class Data(models.Model):
    name = models.CharField(max_length=30)
    phonenumber = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    pic = models.FileField(upload_to = 'profile', default= 'sad.png')

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(Data, on_delete = models.CASCADE)
    content = models.TextField()
    pic = models.FileField(upload_to='blogs', default= 'sad.png')
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.title


class Myride(models.Model):
    date = models.CharField(max_length=20)
    user = models.ForeignKey(Data, on_delete= models.CASCADE)
    pickup_point = models.CharField(max_length=50)
    pickout_point = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    price = models.IntegerField()
    allowed_participants = models.IntegerField()
    arrival_time = models.CharField(max_length=50)
    drop_time = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.pickup_point

class Rideinfo(models.Model):
    pickup_point = models.CharField(max_length=50)
    pickout_point = models.CharField(max_length=50)
    arrival_time = models.CharField(max_length=50)
    drop_time = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    allowed_participants = models.IntegerField()
    price = models.IntegerField()
    ride_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    user = models.ForeignKey(Data, on_delete= models.CASCADE)
    myride = models.ForeignKey(Myride, on_delete= models.CASCADE)

    def __str__(self) -> str:
        return self.pickup_point
        