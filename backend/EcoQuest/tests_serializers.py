from django.test import TestCase
from .serializers import PointOfInterestSerializer as POIS, CategorySerializer as CS, RegisterSerializer as RS, NotificationListSerializer as NLS
from django.contrib.auth.models import User
from .models import  Nomos as N, Perifereia as P, Category, SavedSearch as SE, PointOfInterest as POI

# Create your tests here.

class TestPOISModelSerializer(TestCase):

    def setUp(self) -> None:
        category1 = Category.objects.create(CategoryId=120,Name='natura')
        category2 = Category.objects.create(CategoryId=10,Name='Δάση')
        test = POIS.Meta.model.objects.create(PointOfInterestId=12,Name='John',Longitude=12,Latitude=12)
        test.Categories.add(category1,category2)

    def test_serializer(self):
        test = POIS.Meta.model.objects.get(PointOfInterestId=12)
        json = POIS(test).data
        exdata = {"Name":"John","Categories":[10,120],"Longitude":"12.000000000000000","Latitude":"12.000000000000000",'CreatedDate':json['CreatedDate'],"KeyWords":""}
        jsonexd = exdata
        self.assertEquals(json,jsonexd)

class TestCategoryModelSerializer(TestCase):

    def setUp(self) -> None:
        CS.Meta.model.objects.create(CategoryId=120,Name='nature')

    def test_serializer(self):
        test = CS.Meta.model.objects.get(CategoryId=120)
        json = CS(test).data
        exdata = {"CategoryId":120,"Name":"nature"}
        jsonexd = exdata
        self.assertEquals(json,jsonexd)

class TestNotificationListModelSerializer(TestCase):

    def setUp(self) -> None:
        userid = User.objects.create(username="John",email="john@gmail.com")
        category1 = Category.objects.create(CategoryId=120,Name='natura')
        category2 = Category.objects.create(CategoryId=10,Name='Δάση')
        poiid = POIS.Meta.model.objects.create(Name='John',Longitude=12,Latitude=12)
        poiid.Categories.add(category1,category2)
        NLS.Meta.model.objects.create(NotificationId=10,PointOfInterestId=poiid,UserId=userid,Text="New notification for poi")

    def test_serializer(self):
        test = NLS.Meta.model.objects.get(NotificationId=10)
        json = NLS(test).data
        exdata = {"NotificationId":10,"Text":"New notification for poi","Read":False}
        jsonexd = exdata
        self.assertEquals(json,jsonexd)


class TestRegisterModelSerializer(TestCase):

    def setUp(self) -> None:
        RS.Meta.model.objects.create(id=9,username="Geo",password="aa",email="goe@yahoo.com",first_name="George",last_name="ane")

    def test_serializer(self):
        test = RS.Meta.model.objects.get(id=9)
        json = RS(test).data
        exdata = {"id":9,"username":"Geo","email":"goe@yahoo.com","first_name":"George","last_name":"ane"}
        jsonexd = exdata
        self.assertEquals(json,jsonexd)