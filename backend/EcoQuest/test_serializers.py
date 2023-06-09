from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

import pytest
from .serializers import PointOfInterestSerializer as POIS, CategorySerializer as CS
from .models import  Nomos as N, Perifereia as P, PointOfInterest, Category
from rest_framework.renderers import JSONRenderer

# Create your tests here.

@pytest.mark.usefixtures
def test_poi_serializer() -> None:
    categoryid = Category(CategoryId=120,Name='nature')
    nomosid = N()
    perifereiaid = P()
    test = POIS.Meta.model(Name='John',CategoryId=categoryid,Longitude=12,Latitude=12)
    #print(POIS(test).data)
    json = JSONRenderer().render(POIS(test).data)
    exdata = {"Name":"John","CategoryId":120,"Longitude":"12.000000","Latitude":"12.000000",'CreatedDate': test.CreatedDate}
    jsonexd = JSONRenderer().render(exdata)
    assert json == jsonexd

@pytest.mark.usefixtures
def test_category_serializer() -> None:
    test = CS.Meta.model(CategoryId=120,Name='nature')
    json = JSONRenderer().render(CS(test).data)
    exdata = {"CategoryId":120,"Name":"nature"}
    jsonexd = JSONRenderer().render(exdata)
    assert json == jsonexd