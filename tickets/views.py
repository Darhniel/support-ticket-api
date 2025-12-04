from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404

from .models import Ticket, TicketUpdate
from .serializers import TicketSerializer, TicketUpdateSerializer
from .filters import TicketFilter


class IsSupportOrOwner(permissions.BasePermission):
    """
    Example permission: allow owners and staff to update; everyone authenticated can create.
    """

    def has_object_permission(self, request, view, obj):
        # allow read for owner and staff
        if request.user.is_staff:
            return True
        return obj.created_by == request.user


class TicketViewSet(viewsets.ModelViewSet):
    queryset = (
        Ticket.objects.all()
        .select_related("created_by", "assignee")
        .prefetch_related("updates")
    )
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TicketFilter
    ordering_fields = ["created_at", "priority", "status"]
    search_fields = ["title", "description"]

    def get_permissions(self):
        # for delete forbid non-staff
        if self.action in ("destroy",):
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="add-update")
    def add_update(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketUpdateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(ticket=ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketUpdateViewSet(viewsets.ModelViewSet):
    queryset = TicketUpdate.objects.all().select_related("created_by", "ticket")
    serializer_class = TicketUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
