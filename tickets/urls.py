from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TicketViewSet, TicketUpdateViewSet

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="ticket")
router.register(r"updates", TicketUpdateViewSet, basename="ticketupdate")

urlpatterns = [
    path("", include(router.urls)),
]
