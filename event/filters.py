from django_filters import rest_framework as filters, DateFilter, DateTimeFilter

from event.models import Event


class CustomEventFilter(filters.FilterSet):
    """
    Custom filter class for EventViewSet.
    """
    updated__gte = DateTimeFilter(field_name="event_timestamp", lookup_expr="gte")
    updated__lte = DateTimeFilter(field_name="event_timestamp", lookup_expr="lte")
    rpg_status = filters.CharFilter(field_name="status")
    room_id = filters.UUIDFilter(field_name='room_reservation_id')
    night_of_stay__gte = DateFilter(field_name='night_of_stay', lookup_expr="gte")
    night_of_stay__lte = DateFilter(field_name='night_of_stay', lookup_expr="lte")

    class Meta:
        model = Event
        fields = [
            "hotel_id",
            "updated__gte",
            "updated__lte",
            "rpg_status",
            "room_id",
            "night_of_stay__gte",
            "night_of_stay__lte",
        ]
