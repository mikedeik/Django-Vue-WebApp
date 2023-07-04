from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PointOfInterest, SavedSearch, Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=PointOfInterest)
def poi_created(sender, instance, created, **kwargs):
    if created:
        print("running")
        notification_text = f"New POI '{instance.Name}'"
        create_notification(notification_text, instance)


# For every search in the database create a notification
def create_notification(notification_text, instance):
    categories = instance.Categories.all()
    print(categories)
    saved_searches = SavedSearch.objects.all().filter(Categories__in=categories)
    if saved_searches:
        for search in saved_searches:
            notification = Notification(UserId=search.UserId,
                                        PointOfInterestId=instance,
                                        Text=notification_text)
            notification.save()

            notification_data = {
                'id': notification.NotificationId,
                'message': notification.Text
            }

            channel_layer = get_channel_layer()
            print(channel_layer)
            event = {
                'type': 'message',
                'data': notification_data
            }
            print("all good here")
            print(search.UserId.id)
            async_to_sync(channel_layer.group_send)(
                f"user_{search.UserId.id}",
                event
            )
    # print(notification)

    # url = 'http://localhost:5137/webhook/'
    # payload = {'notification': notification}
    # requests.post(url, data=payload)