from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from event.models import Event


class EventSerializer(ModelSerializer):
    """
    Serializer class for serializing Event objects for read operations and input data validation.
    """
    hotel_id = serializers.IntegerField()
    timestamp = serializers.DateTimeField(source="event_timestamp", read_only=True)
    rpg_status = serializers.ChoiceField(choices=[1, 2], source="status")
    room_id = serializers.UUIDField(source="room_reservation_id")
    night_of_stay = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Event
        fields = ["id", "hotel_id", "timestamp", "rpg_status", "room_id", "night_of_stay"]
