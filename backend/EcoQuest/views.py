from django.shortcuts import render
from .models import Category, PointOfInterest
from .serializers import PointOfInterestSerializer, CategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication


# Create your views here.

class CategoryList(APIView):

    def get(self, request):
        categories = Category.objects.all()
        print(categories)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

