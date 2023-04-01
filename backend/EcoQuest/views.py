from django.shortcuts import render
from .models import Category, PointOfInterest, Notification
from .serializers import PointOfInterestSerializer, CategorySerializer, NotificationListSerializer, \
    NotificationPutSerializer
from django.contrib.auth.models import User

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


class NotificationsList(APIView):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        print(user.id)
        notifications = Notification.objects.all().filter(Retrieved=False)
        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationRead(APIView):

    def put(self, request, NotificationId):
        notification = Notification.objects.get(NotificationId=NotificationId)
        serializer = NotificationPutSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)