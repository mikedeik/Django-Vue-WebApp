from django.urls import path
from .views import CategoryList, NotificationsList, NotificationRead

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('notifications/', NotificationsList.as_view()),
    path('notifications/<int:NotificationId>/', NotificationRead.as_view()),
]

