from django.urls import path

# '/flight/':
urlpatterns = [
]

# ---------- Router ----------
from rest_framework.routers import DefaultRouter
from .views import (
    PassengerView,
    FlightView,
    ReservationView
)
router = DefaultRouter()
router.register('passenger', PassengerView)
router.register('flight', FlightView)
router.register('reservation', ReservationView)
urlpatterns += router.urls