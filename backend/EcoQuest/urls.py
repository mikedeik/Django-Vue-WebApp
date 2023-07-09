from django.urls import path
from .views import CategoryList, NotificationsList, NotificationRead, PoIList, PoIDetails, \
    CreatePOIsAPIView, CreateCategory, CreatePoiApi, RegisterView, SavedSearchCreate, SearchPoisView

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('post/categories/', CreateCategory.as_view()),
    path('searches/', SavedSearchCreate.as_view()),
    path('notifications/', NotificationsList.as_view()),
    path('notifications/<int:NotificationId>/', NotificationRead.as_view()),
    path('create_pois/', CreatePOIsAPIView.as_view(), name='create_pois'),
    path('post/poi/', CreatePoiApi.as_view()),
    path('poi/', PoIList.as_view()),
    path('search/pois/', SearchPoisView.as_view()),

    path('poi/<int:PoIID>/', PoIDetails.as_view()),

]

