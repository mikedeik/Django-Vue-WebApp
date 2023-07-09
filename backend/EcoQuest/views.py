import io
import pandas as pd
import math
# from geopy import distance
from geopy.distance import geodesic
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


class AddToFavorites(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, PoiId):
        user = User.objects.get(id=request.user.id)
        poi = PointOfInterest.objects.get(PointOfInterestId=PoiId)
        if request.data['favorite']:
            poi.IsFavoriteTo.add(user)
        else:
            poi.IsFavoriteTo.remove(user)
        return Response({"PointOfInterestId": poi.PointOfInterestId}, status=status.HTTP_202_ACCEPTED)




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


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'count'
    max_page_size = 100


class SearchPoisView(APIView):

    def post(self, request):
        body = request.data
        text = body.get('text', '')
        filters = body.get('filters', {})
        long = None
        lat = None
        km = None
        distance = None
        category_array = []
        keywords = []

        try:
            page = body.get('page', 1)
            count = body['count']

            # if filters are given
            if not filters == {}:

                distance = filters.get('distance', {})

                # get distance filters if any
                if not distance == {}:
                    long = distance['lon']
                    lat = distance['lat']
                    km = distance['km']

                # get categories if any
                category_array = filters.get('categories', [])

                # get keywords if any
                keywords = filters.get('keywords', [])


            # build the base query to filter PointOfInterest objects
            query = PointOfInterest.objects.all()

            # create query for text based on the 'Name', 'Perifereia', and 'Nomos' fields
            if text:
                print(text)
                text_query = Q(Name__contains=text) | Q(PerifereiaId__Name__contains=text) | Q(
                    NomosId__Name__contains=text) | Q(Description__contains=text)
            else:
                text_query = Q()

            # create query for categories
            category_query = Q()
            if category_array:
                category_query = Q(Categories__in=category_array)

            keyword_queries = Q()
            if keywords:
                for keyword in keywords:
                    keyword_queries |= Q(KeyWords__icontains=keyword.lower())

            # get pois for a specific distance in kms
            # distance_queryset = Q()
            if lat is not None and long is not None and km is not None:

                #check types of values
                if not isinstance(lat, float) or not isinstance(long, float):
                    raise ValueError("lat and lon must be of type float")   #handle the error or raise an exception
                if km is not None:
                    if not isinstance(km, int):
                        raise ValueError("km must be of type int")  #handle the error or raise an exception

                #filter objects based on exact distance
                points_of_interest = PointOfInterest.objects.all()
                filtered_points = []
                target_location = (lat, long)
                for poi in points_of_interest:
                    poi_location = (poi.Latitude, poi.Longitude)
                    distance = geodesic(target_location, poi_location).kilometers
                    if distance == 0.0 or abs(distance - km) < 0.001:  #if the distance is spot on or if too small add it to filtered pois
                        filtered_points.append(poi)

                #convert list of objects into a QuerySet
                if not filtered_points == []:
                    filtered_pks = [fp.PointOfInterestId for fp in filtered_points]
                    distance_queryset = PointOfInterest.objects.filter(PointOfInterestId__in=filtered_pks) #actual conversion


            ###########################################
            # perform the final query
            print(category_array)
            print(text)
            if text == '' and not category_array == [] and not keywords == []:
                print("here")
                if not distance == {} and distance is not None:
                    query = distance_queryset
                else:
                    query = PointOfInterest.objects.none()

            query = query.filter(text_query).filter(category_query).filter(keyword_queries).distinct()

            paginator = CustomPagination()
            paginated_query = paginator.paginate_queryset(query, request)

            #serialize the paginated results
            serializer = PointOfInterestSerializer(paginated_query, many=True)

            #return the paginated response
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'exception': e}, status=500)


class FavoritesList(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        pois = PointOfInterest.objects.all().filter(IsFavoriteTo=user)
        serializer = PointOfInterestSerializer(pois, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
                description = df.loc[row_num, 'description']
                try:
                    poi = PointOfInterest(
                        Name=name,
                        PerifereiaId_id=perifereia_id,
                        NomosId_id=nomos_id,
                        Longitude=longitude,
                        Latitude=latitude,
                        KeyWords=keywords,
                        Description = description
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
