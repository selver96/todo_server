from unicodedata import category
from django.contrib import auth
from rest_framework import serializers
from .models import *


class RegistrationsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegistrationSuperUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):

        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # username = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'access', 'refresh']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        user = auth.authenticate(email=email, password=password)
        
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'id': user.id,
            'access': user.access,
            'refresh': user.refresh
        }


class LogoutSerializer(serializers.ModelSerializer):
    access = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'token']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = auth.logout(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }


class TaskGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskGroup
        fields = ['id', 'title']


class TaskSerializer:

    def __init__(self, obj):
        self.data = list()
        self.obj = obj

    def get_group_task(self):
        for item in self.obj:
            group = dict()
            group["id"] = item.group.id
            group["title"] = item.group.title
            group["for_completed"] = item.group.for_completed
            group["tasks"] = self.get_task(item.group.id)
            if group not in self.data:
                self.data.append(group)

    def get_task(self, _id):
        tasks = []
        for item in self.obj:
            task = dict()
            if item.group.id == _id:
                task["id"] = item.id
                task["title"] = item.title
                task["is_completed"] = item.is_completed
                task["end_at"] = item.end_at
                tasks.append(task)
        return tasks

    def add_group_task(self, array, obj):
        
        for item in obj:
            in_ = False
            for i in array:
                if i["id"] == item.id:
                    in_ = True
            if in_ == False:
                group = dict()
                group["id"] = item.id
                group["title"] = item.title
                group["tasks"] = list()
                array.append(group)
        return array
