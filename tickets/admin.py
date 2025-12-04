from django.contrib import admin
from .models import Ticket, TicketUpdate


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "priority",
        "created_by",
        "assignee",
        "created_at",
    )
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "description")


@admin.register(TicketUpdate)
class TicketUpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "created_by", "is_internal", "created_at")
    list_filter = ("is_internal", "created_at")
