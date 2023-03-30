from django.contrib import admin

from .models import Category, PointOfInterest, Nomos, Perifereia, PoiPicture, SavedSearch
# Register your models here.

admin.site.register(Category)
admin.site.register(PointOfInterest)
admin.site.register(Nomos)
admin.site.register(Perifereia)
admin.site.register(PoiPicture)
admin.site.register(SavedSearch)


