from django.test import TestCase, Client
from .models import PointOfInterest, Category , Perifereia, Nomos
from .serializers import PointOfInterestSerializer as POIS
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import pandas as pd

class TestPoiListView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        category1 = Category.objects.create(CategoryId=12,Name='natura')
        category2 = Category.objects.create(CategoryId=10,Name='Δάση')
        pois = PointOfInterest.objects.bulk_create([PointOfInterest(PointOfInterestId=12,Name='John',Longitude=12,Latitude=12), 
        PointOfInterest(PointOfInterestId=19,Name='Gianni',Longitude=12,Latitude=12) ])
        pois.pop().Categories.add(category1,category2)

    def test_poilist_view(self):
        data = PointOfInterest.objects.all()
        testdata = POIS(data, many=True).data
        response = self.client.get("/ecoquest/poi/")
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.data,testdata)


class TestPoiDetailsView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        category1 = Category.objects.create(CategoryId=1,Name='natura')
        category2 = Category.objects.create(CategoryId=2,Name='dasi')
        poi = PointOfInterest.objects.create(PointOfInterestId=12,Name='John',Longitude=12,Latitude=12)
        poi.Categories.add(category1,category2)

    def test_poidetails_view(self):
        testdata = POIS(PointOfInterest.objects.get(PointOfInterestId=12)).data
        response = self.client.get("/ecoquest/poi/12/")
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.data,testdata)

class TestCreatePOIsAPIView(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_createpoisapi_view(self):
        filename = {"myfile":"LimnesElladas"}
        response = self.client.post("/ecoquest/create_pois/"+filename['myfile']+"/",filename)
        self.assertNotEquals(response,200)


class TestCreatePoiAPI(TestCase):

    def setUp(self):
        self.client = Client()
        category1 = Category.objects.create(CategoryId=4,Name='natura')
        category2 = Category.objects.create(CategoryId=7,Name='dasi')
        nomos = Nomos.objects.create()
        perifereia = Perifereia.objects.create()
        poi = PointOfInterest.objects.create(PointOfInterestId=12,Name='Megalo Elato',NomosId=nomos,PerifereiaId=perifereia,Longitude=12,Latitude=12)
        poi.Categories.add(category1,category2)

    def test_createpoiapi_view(self):
        testdata = POIS(PointOfInterest.objects.get(PointOfInterestId=12)).data
        response = self.client.post("/ecoquest/post/poi/",testdata)
        self.assertNotEquals(response.status_code,200)
