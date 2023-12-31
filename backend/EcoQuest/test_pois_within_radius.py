from django.test import TestCase
from .models import Category, SavedSearch
from django.contrib.auth.models import User
from .serializers import PointOfInterestSerializer as POIS
from scripts.CheckInside import pois_within_radius

class Testpois_within_radius(TestCase):

    def setUp(self) -> None:
        category1 = Category.objects.create(CategoryId=120, Name='natura')
        category2 = Category.objects.create(CategoryId=10, Name='Dasi')
        data = POIS.Meta.model.objects.create(PointOfInterestId=12, Name='Megalo Dasos', Longitude=6, Latitude=1)
        data.Categories.add(category1,category2)
        userid = User.objects.create()
        savedsearch = SavedSearch.objects.create(SavedSearchId=7, UserId=userid, Radius=900)
        savedsearch.Categories.add(category1,category2)

    
    def test_pois_within_radius(self):
        pois = POIS.Meta.model.objects.all()
        savedsearch = SavedSearch.objects.get(SavedSearchId=7)
        for poi in pois:
            testdata = pois_within_radius(poi, savedsearch)
        self.assertEquals(testdata, True)
