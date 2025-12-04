import django_filters
from .models import Ticket


class TicketFilter(django_filters.FilterSet):
    created_by = django_filters.NumberFilter(field_name="created_by__id")
    assignee = django_filters.NumberFilter(field_name="assignee__id")
    status = django_filters.CharFilter(field_name="status")
    priority = django_filters.CharFilter(field_name="priority")
    created_after = django_filters.IsoDateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.IsoDateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    class Meta:
        model = Ticket
        fields = [
            "status",
            "priority",
            "assignee",
            "created_by",
            "created_after",
            "created_before",
        ]
