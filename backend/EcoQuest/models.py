from django.db import models
# Create your models here.


class Category(models.Model):
    CategoryId = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=100, unique=True)


class PointOfInterest(models.Model):
    PointOfInterestId = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=100, unique=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)




