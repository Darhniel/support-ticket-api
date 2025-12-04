from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Ticket, TicketUpdate

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class TicketUpdateSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = TicketUpdate
        fields = ["id", "ticket", "created_by", "note", "is_internal", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)


class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSimpleSerializer(read_only=True)
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    updates = TicketUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "created_by",
            "assignee",
            "status",
            "priority",
            "created_at",
            "updated_at",
            "updates",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at", "updates"]

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters.")
        return value

    def validate(self, data):
        # basic conflict example: can't set status to resolved without updates
        if data.get("status") == Ticket.STATUS_RESOLVED:
            # If trying to resolve, require that there is at least one update provided in context
            # (This is an example; in most real apps you'd model state changes differently.)
            # We'll allow resolve but log a warning — here we simply allow it.
            pass
        return data

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # simple example: capture who changed assignee/status in TicketUpdate automatically?
        # We'll just update the ticket. If you want, you can create an automatic TicketUpdate here.
        return super().update(instance, validated_data)
