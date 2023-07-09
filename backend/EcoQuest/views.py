import io
import pandas as pd
from django.db.models import Q
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Category, PointOfInterest, Notification, SavedSearch
from .serializers import PointOfInterestSerializer, CategorySerializer, NotificationListSerializer, \
    NotificationPutSerializer, RegisterSerializer, SavedSearchSerializer
from django.contrib.auth.models import User
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
import codecs
from rest_framework import generics
from scripts.preprocess_csv import preprocess
from django.core.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination



# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    permission_classes = [AllowAny]

    def get(self, request):

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    
class SavedSearchCreate(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = SavedSearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['UserId'] = user

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationsList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
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


class SearchPoisView(APIView):
    pagination_class = PageNumberPagination

    def post(self, request):
        body = request.data
        text = body.get('text', '')
        filters = body.get('filters', {})


        try:
            page = body.get('start', 1)
            count = body['count']

            print(body)
            print(page)
            print(count)
            print(text)
            print(filters)

            #if filters are given
            if not filters == {}:
                distance = filters.get('distance', {})

                #get distance filters if any
                if not distance == {}:
                    long = distance['lon']
                    lat = distance['lat']
                    km = distance['km']
                    print(long)
                    print(lat)
                    print(km)

                #get categories if any
                category_array = filters.get('categories', [])

                #get keywords if any
                keywords = filters.get('keywords', [])

                print(keywords)
                print(category_array)
                

        except Exception as e:
            print(0)
            return Response({'exception': e}, status=500)
        return Response()######


        


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

            df = preprocess(tsv_file, file.name)
            pois_to_create = []
            errors = []
            #insert data from dataframe produced from the script
            for row_num in range(len(df)):

                name = df.loc[row_num, 'name']
                perifereia_id = df.loc[row_num, 'perifereia']
                nomos_id = df.loc[row_num, 'nomos']
                longitude = df.loc[row_num, 'longitude']
                latitude = df.loc[row_num, 'latitude']
                keywords = df.loc[row_num, 'keywords']
                try:
                    poi = PointOfInterest(
                        Name=name,
                        PerifereiaId_id=perifereia_id,
                        NomosId_id=nomos_id,
                        Longitude=longitude,
                        Latitude=latitude,
                        KeyWords=keywords
                    )
                    poi.full_clean()  # Run model field validation
                    pois_to_create.append(poi)
                except ValidationError as e:
                    error_message = str(e)
                    return render(request, 'myapp/error_template.html', {'error_message': error_message})
                except Exception as e:
                    errors.append(f"Error creating PointOfInterest: {str(e)}")
            if errors:
                return Response({'errors': errors}, status=400)
            else:
                # Commit the changes to the database
                PointOfInterest.objects.bulk_create(pois_to_create)
                
                for poi in pois_to_create:
                    poi.save()
                
                # Insert category ids for each poi
                #convert dataframe column to list 
                category_ids = df['categories'].tolist()

                created_pois_ids = [poi.PointOfInterestId for poi in pois_to_create]

                for poi, pois_category_ids in zip(pois_to_create, category_ids):
                    categories = Category.objects.filter(CategoryId__in=pois_category_ids)

                    poi.Categories.set(categories.filter(CategoryId__in = pois_category_ids))
                
                return Response({'message': 'Points of Interest created successfully', 'created_pois': created_pois_ids})
            tsv_file.close()
        else:
            return Response({'error': 'No file provided.'}, status=400)
