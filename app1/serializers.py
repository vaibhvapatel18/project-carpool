from rest_framework import serializers
from .models import Data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['id','name','phonenumber','email']