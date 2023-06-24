from django.test import TestCase, Client
from .views import PoIList, RegisterView, CreatePOIsAPIView, PoIDetails
from .models import PointOfInterest, Category
from django.contrib.auth.models import User

class TestPoiListView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        categoryid = Category.objects.create(CategoryId=120,Name='nature')
        [ PointOfInterest.objects.create(PointOfInterestId=12,Name='John',CategoryId=categoryid,Longitude=12,Latitude=12),
          PointOfInterest.objects.create(PointOfInterestId=19,Name='Gianni',CategoryId=categoryid,Longitude=12,Latitude=12) ]
    
    def test_poilist_view(self):
        response = self.client.get("/ecoquest/poi/")
        self.assertEquals(response.status_code,200)

class TestPoiDetailsView(TestCase):

    def setUp(self):
        self.client = Client()
        categoryid = Category.objects.create(CategoryId=120,Name='nature')
        PointOfInterest.objects.create(PointOfInterestId=12,Name='John',CategoryId=categoryid,Longitude=12,Latitude=12)

    def test_poidetails_view(self):
        response = self.client.get("/ecoquest/poi/12/")
        self.assertEquals(response.status_code,200)

class TestNotificationListView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_notificationlist_view(self):
        response = self.client.get("/ecoquest/notifications/")
        self.assertEquals(response.status_code,200)