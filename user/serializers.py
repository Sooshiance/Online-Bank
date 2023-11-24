from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User, Profile


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = User
        fields = ("id", "phone", "email", "first_name", "last_name")


class UserRegisterationSerializer(serializers.ModelSerializer):
    """ 
    Serializer class to serialize registration requests and create a new user.
    """
    
    class Meta:
        model = User
        fields = ("id", "phone", "email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class ProfileSerializer(CustomUserSerializer):
    """
    Serializer class to serialize the user Profile model
    """

    class Meta:
        model = Profile
        fields = ("email", "phone", "first_name", "last_name")
