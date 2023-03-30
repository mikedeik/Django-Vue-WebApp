from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PointOfInterest
import requests


@receiver(post_save, sender=PointOfInterest)
def poi_created(sender, instance, created, **kwargs):
    if created:
        notification = f"New POI '{instance.Name}'"
        send_notification(notification)


def send_notification(notification):
    print(notification)
    # url = 'http://localhost:5137/webhook/'
    # payload = {'notification': notification}
    # requests.post(url, data=payload)