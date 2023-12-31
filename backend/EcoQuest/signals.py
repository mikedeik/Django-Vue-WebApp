from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import PointOfInterest, SavedSearch, Notification, Category
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from scripts.CheckInside import pois_within_radius


@receiver(m2m_changed, sender=PointOfInterest.Categories.through)
def poi_categories_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        if not reverse:
            # Get the full set of categories
            categories = Category.objects.filter(pk__in=pk_set)
            notification_text = f"Νέα Περιοχή Ενδιαφέροντος '{instance.Name}'"
            create_notification(notification_text, instance, categories)


# For every search in the database create a notification
def create_notification(notification_text, instance, categories):

    saved_searches = SavedSearch.objects.all().filter(Categories__in=categories).distinct()
    if saved_searches:
        for search in saved_searches:
            if pois_within_radius(instance, search):
                notification = Notification(UserId=search.UserId,
                                            PointOfInterestId=instance,
                                            Text=notification_text)
                notification.save()

                notification_data = {
                    'id': notification.NotificationId,
                    'title': 'Μόλις Δημιουργήθηκε Μια νέα Περιοχή',
                    'message': notification.Text,
                    'PoiId': instance.PointOfInterestId
                }

                channel_layer = get_channel_layer()
                event = {
                    'type': 'message',
                    'data': notification_data
                }

                async_to_sync(channel_layer.group_send)(
                    f"user_{search.UserId.id}",
                    event
                )
    # print(notification)

    # url = 'http://localhost:5137/webhook/'
    # payload = {'notification': notification}
    # requests.post(url, data=payload)