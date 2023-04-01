from abc import ABC

from rest_framework import serializers
from .models import Category, PointOfInterest, Notification


class PointOfInterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PointOfInterest
        fields = ['PointOfInterestId', 'Name', 'Category']


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




