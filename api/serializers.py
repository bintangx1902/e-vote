from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leader
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    leader = LeaderSerializer()

    class Meta:
        model = Candidate
        fields = '__all__'


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, clean_data):
        username = clean_data.get('username')
        password = clean_data.get('password')
        email = clean_data.get('email')
        f_name = clean_data.get('first_name')
        l_name = clean_data.get('last_name')

        instance = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=f_name,
            last_name=l_name,
            is_active=True
        )
        return instance


# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#
#     def check_user(self, clean_data):
#         username = clean_data.get('username')
#         password = clean_data.get('password')
#
#         user = authenticate(self, username=username, password=password)
#         if not user:
#             raise ValidationError('User not Found!')
#         return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        # extra_kwargs = {'password': {'write_only': True}}