
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User


# Create your models here.

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email', 'is_admin']