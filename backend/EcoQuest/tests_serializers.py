from django.test import TestCase
from .serializers import PointOfInterestSerializer as POIS, CategorySerializer as CS
from .models import  Nomos as N, Perifereia as P, PointOfInterest, Category
from rest_framework.renderers import JSONRenderer

# Create your tests here.

class TestModelSerializer(TestCase):

    def setUp(self) -> None:
        categoryid = Category.objects.create(CategoryId=120,Name='nature')
        nomosid = N.objects.create()
        perifereiaid = P.objects.create()
        test = POIS.Meta.model.objects.create(Name='John',CategoryId=categoryid,Longitude=12,Latitude=12)

    def test_serializer(self,) -> int:
        test = POIS.Meta.model.objects.get(CategoryId=120)
        #print(POIS(test).data)
        json = JSONRenderer().render(POIS(test).data)
        exdata = {"Name":"John","CategoryId":120,"Longitude":"12.000000","Latitude":"12.000000",'CreatedDate': test.CreatedDate}
        jsonexd = JSONRenderer().render(exdata)
        self.assertEquals(json,jsonexd)