from abc import ABC
from rest_framework import serializers
from .models import Category, PointOfInterest, Notification, SavedSearch
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class PointOfInterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PointOfInterest
        fields = '__all__'
        # fields = ['Name', 'Categories', 'Longitude', 'Latitude', 'CreatedDate', 'KeyWords']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['CategoryId', 'Name']


class NotificationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['NotificationId', 'Text', 'Read']


class NotificationPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['Retrieved']


class SavedSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedSearch
        fields = ['Categories', 'CenterLatitude', 'CenterLongitude', 'Radius']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


