from datetime import datetime

import factory
from dateutil.tz import UTC
from factory import Faker
from factory.fuzzy import FuzzyNaiveDateTime, FuzzyDateTime, FuzzyInteger

from event.models import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    room_reservation_id = Faker('uuid4')
    night_of_stay = FuzzyNaiveDateTime(datetime(2024, 1, 1))
    status = Event.BOOKING
    event_timestamp = FuzzyDateTime(datetime(2023, 1, 1, tzinfo=UTC))
    hotel_id = FuzzyInteger(42)
