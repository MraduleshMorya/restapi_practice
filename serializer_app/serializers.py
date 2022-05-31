from typing_extensions import Required
from rest_framework import serializers
from django.db import models
from setuptools import Require
from .models import Employee,Employee2


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['username', 'first_name', 'last_name', 'email', 'department']
        
        
class EmployeeSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['username', 'email']
        
        
class EmployeeSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['password']


class Employee2Serializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    first_name =  serializers.CharField(max_length=20, required=False)
    last_name = serializers.CharField(max_length=10, required= False)
    department = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(max_length=30)
    password  = serializers.CharField(max_length=40, default='1')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Employee2.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.department = validated_data.get('department', instance.department)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


# https://github.com/MraduleshMorya/Ecom2
# https://github.com/MraduleshMorya/Django_restapi_practice
# https://github.com/MraduleshMorya/Django_restapi_practice.git