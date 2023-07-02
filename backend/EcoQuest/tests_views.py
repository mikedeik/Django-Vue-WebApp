from django.test import TestCase, Client
from .models import PointOfInterest, Category
from .serializers import PointOfInterestSerializer as POIS
from django.contrib.auth.models import User

class TestPoiListView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        categoryid = Category.objects.create(CategoryId=120,Name='nature')
        PointOfInterest.objects.bulk_create([PointOfInterest(PointOfInterestId=12,Name='John',CategoryId=categoryid,Longitude=12,Latitude=12), 
        PointOfInterest(PointOfInterestId=19,Name='Gianni',CategoryId=categoryid,Longitude=12,Latitude=12) ])

    def test_poilist_view(self):
        data = PointOfInterest.objects.all()
        testdata = POIS(data, many=True).data
        response = self.client.get("/ecoquest/poi/")
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.data,testdata)


class TestPoiDetailsView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        categoryid = Category.objects.create(CategoryId=120,Name='nature')
        self.data = PointOfInterest.objects.create(PointOfInterestId=12,Name='John',CategoryId=categoryid,Longitude=12,Latitude=12)

    def test_poidetails_view(self):
        testdata = POIS(PointOfInterest.objects.get(PointOfInterestId=12)).data
        response = self.client.get("/ecoquest/poi/12/")
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.data,testdata)