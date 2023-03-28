from django.contrib import admin

from .models import Category, PointOfInterest
# Register your models here.

admin.site.register(Category)
admin.site.register(PointOfInterest)

