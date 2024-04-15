import uuid

from django.db import models


class Event(models.Model):
    """
    Model representing an event.
    """

    RPG_STATUS_CHOICES = [
        (BOOKING := 1, "booking"),
        (CANCELLATION := 2, "cancellation")
    ]

    room_reservation_id = models.UUIDField(default=uuid.uuid4)
    night_of_stay = models.DateField()
    status = models.IntegerField(choices=RPG_STATUS_CHOICES)
    event_timestamp = models.DateTimeField(auto_now=True)
    hotel_id = models.CharField(max_length=16)
