from django.test import TestCase, Client
from .models import PointOfInterest, Category
from .serializers import PointOfInterestSerializer as POIS
from django.contrib.auth.models import User

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
        category2 = Category.objects.create(CategoryId=2,Name='Δάση')
        poi = PointOfInterest.objects.create(PointOfInterestId=12,Name='John',Longitude=12,Latitude=12)
        poi.Categories.add(category1,category2)

    def test_poidetails_view(self):
        testdata = POIS(PointOfInterest.objects.get(PointOfInterestId=12)).data
        response = self.client.get("/ecoquest/poi/12/")
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.data,testdata)