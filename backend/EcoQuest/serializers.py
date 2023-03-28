from abc import ABC

from rest_framework import serializers
from .models import Category, PointOfInterest


class PointOfInterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PointOfInterest
        fields = ['PointOfInterestId', 'Name', 'Category']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['CategoryId', 'Name']




