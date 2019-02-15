from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TripViewSet, TripDayViewSet

router = DefaultRouter()
router.register('trip', TripViewSet)
router.register('trip_day', TripDayViewSet)

app_name = 'trip'

urlpatterns = [
    path('', include(router.urls)),
]
