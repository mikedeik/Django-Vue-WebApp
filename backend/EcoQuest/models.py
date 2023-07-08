import time
from math import radians, cos, sin, asin, sqrt

EARTH_RADIUS_KM = 6371

from django.db import models
# from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User
from django.utils import timezone
# from django.contrib.gis.geos import Point
# Create your models here.


def upload_to(instance, filename):
    return f'{filename}'.format(filename=filename)


class Category(models.Model):
    CategoryId = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.Name


class Nomos(models.Model):
    NomosId = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.Name


class Perifereia(models.Model):
    PerifereiaId = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.Name


class PointOfInterest(models.Model):
    PointOfInterestId = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=250, unique=False)
    Categories = models.ManyToManyField(Category)
    PerifereiaId = models.ForeignKey(Perifereia, on_delete=models.CASCADE, null=True, blank=True)
    NomosId = models.ForeignKey(Nomos, on_delete=models.CASCADE, null=True, blank=True)
    Longitude = models.DecimalField(max_digits=18, decimal_places=15)
    Latitude = models.DecimalField(max_digits=18, decimal_places=15)
    #TODO connect to another db to be able to use Points
    # location = gis_models.PointField(default=Point(0, 0))
    CreatedDate = models.DateTimeField(default=timezone.now)
    KeyWords = models.CharField(max_length=2000, default="")

    def __str__(self):
        return self.Name


class PoiPicture(models.Model):
    PoiPictureId = models.BigAutoField(primary_key=True)
    Picture = models.ImageField(upload_to=upload_to, null=True, blank=True)
    PointOfInterestId = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE)

    def __str__(self):
        return self.PoiPictureId


class SavedSearch(models.Model):
    SavedSearchId = models.BigAutoField(primary_key=True)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Categories = models.ManyToManyField(Category)
    CenterLatitude = models.DecimalField(max_digits=18, decimal_places=15, default= 0.000000000000000)
    CenterLongitude = models.DecimalField(max_digits=18, decimal_places=15, default= 0.000000000000000)
    Radius = models.DecimalField(max_digits=18, decimal_places=15)
    CreatedDate = models.DateTimeField(default=timezone.now)


class Notification(models.Model):
    NotificationId = models.BigAutoField(primary_key=True)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    PointOfInterestId = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE)
    Text = models.CharField(max_length=1000)
    Read = models.BooleanField(default=False)
    Retrieved = models.BooleanField(default=False)
    CreatedDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Text



