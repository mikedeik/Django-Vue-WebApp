import io
import pandas as pd
from django.shortcuts import render
from .models import Category, PointOfInterest, Notification
from .serializers import PointOfInterestSerializer, CategorySerializer, NotificationListSerializer, \
    NotificationPutSerializer, RegisterSerializer
from django.contrib.auth.models import User
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser,FormParser
import codecs
from rest_framework import generics
from scripts.preprocess_csv import preprocess
from django.core.exceptions import ValidationError

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Create your views here.

class CreateCategory(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.username != 'admin':
            return Response({'message': 'Unauthorized'}, status=403)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CreatePoiApi(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.username != 'admin':
            return Response({'message': 'Unauthorized'}, status=403)
        serializer = PointOfInterestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
        

class CategoryList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        categories = Category.objects.all()
        print(categories)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    


class NotificationsList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        print(user.id)
        notifications = Notification.objects.all().filter(Retrieved=False)
        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationRead(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, NotificationId):
        notification = Notification.objects.get(NotificationId=NotificationId)
        serializer = NotificationPutSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List of Pois

class PoIList(APIView):

    def get(self, request):
        poi = PointOfInterest.objects.all()
        serializer = PointOfInterestSerializer(poi, many=True)
        return Response(serializer.data)


# Details of PoI

class PoIDetails(APIView):

    
    # Define custom function to raise exception if PoI was not found
    def get_object(self, PoIID):
        try:
            return PointOfInterest.objects.get(PointOfInterestId=PoIID)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, PoIID):
        poi = self.get_object(PoIID)
        serializer = PointOfInterestSerializer(poi)
        return Response(serializer.data)


class CreatePOIsAPIView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        file = request.data['myfile']
        if file:
            if not file.name.endswith('.tsv') and not file.name.endswith('.csv'):
                return Response({'error': 'Invalid file format. Only TSV files are allowed.'}, status=400)


            # Read the uploaded file data using io.StringIO
            tsv_data = file.read().decode('utf-8')
            tsv_file = io.StringIO(tsv_data)

            # reader = csv.reader(tsv_file, delimiter='\t')
            print(tsv_file)
            df = preprocess(tsv_file)
            pois_to_create = []
            errors = []
            # for row_num, row in enumerate(reader, start=1):
            #insert data from dataframe produced from the script
            for row_num in range(len(df)):
                print(row_num)
                print(df.loc[row_num])
                # if len(row) != 6:
                #     errors.append(f"Invalid number of columns at row {row_num}")
                #     continue
                name = df.loc[row_num, 'name']
                category_id = df.loc[row_num, 'category']
                perifereia_id = df.loc[row_num, 'perifereia']
                nomos_id = df.loc[row_num, 'nomos']
                longitude = df.loc[row_num, 'longitude']
                latitude = df.loc[row_num, 'latitude']
                try:
                    poi = PointOfInterest(
                        Name=name,
                        CategoryId_id=category_id,
                        PerifereiaId_id=perifereia_id,
                        NomosId_id=nomos_id,
                        Longitude=longitude,
                        Latitude=latitude
                    )
                    print("BEFORE VALIDATION")
                    poi.full_clean()  # Run model field validation
                    print("AFTER VALIDATION")
                    pois_to_create.append(poi)
                    print("POI APPENDED@@@@@@@@")
                except ValidationError as e:
                    error_message = str(e)
                    return render(request, 'myapp/error_template.html', {'error_message': error_message})
                # except Exception as e:
                #     errors.append(f"Error creating PointOfInterest at row {row_num}: {str(e)}")
            if errors:
                return Response({'errors': errors}, status=400)
            else:
                # Commit the changes to the database
                print("BULKINGGGGGGGGGGGGG")
                PointOfInterest.objects.bulk_create(pois_to_create)
                created_pois_ids = [poi.PointOfInterestId for poi in pois_to_create]
                return Response({'message': 'Points of Interest created successfully', 'created_pois': created_pois_ids})
            tsv_file.close()
        else:
            return Response({'error': 'No file provided.'}, status=400)
