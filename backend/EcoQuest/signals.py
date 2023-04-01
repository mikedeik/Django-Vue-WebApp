from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PointOfInterest, SavedSearch, Notification
from django.contrib.auth.models import User
import requests


@receiver(post_save, sender=PointOfInterest)
def poi_created(sender, instance, created, **kwargs):
    if created:
        notification_text = f"New POI '{instance.Name}'"
        create_notification(notification_text, instance)

# For every search in the database create a notification
def create_notification(notification_text, instance):

    saved_searches = SavedSearch.objects.all().filter(CategoryId=instance.CategoryId)
    if saved_searches:
        for search in saved_searches:
            notification = Notification(UserId=search.UserId, PointOfInterestId=instance,
                                        Text=notification_text)
            notification.save()

    # print(notification)

    # url = 'http://localhost:5137/webhook/'
    # payload = {'notification': notification}
    # requests.post(url, data=payload)