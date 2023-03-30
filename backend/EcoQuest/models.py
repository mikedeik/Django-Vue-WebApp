from django.db import models
from django.contrib.auth.models import User
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
    Name = models.CharField(max_length=100, unique=True)
    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    PerifereiaId = models.ForeignKey(Perifereia, on_delete=models.CASCADE, null=True, blank=True)
    NomosId = models.ForeignKey(Nomos, on_delete=models.CASCADE, null=True, blank=True)

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
    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    Radius = models.FloatField()



