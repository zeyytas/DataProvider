from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import AccessToken
from uuid import uuid4

from event.models import Event
from event.tests.factories.event import EventFactory
from event.tests.factories.user import UserFactory


class EventAPITests(APITestCase):
    """Test cases for the Event API endpoints."""
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.event_1 = EventFactory(
            hotel_id=1,
            night_of_stay="2022-01-01",
            status=Event.BOOKING,
        )
        cls.event_2 = EventFactory(
            hotel_id=2,
            night_of_stay="2023-01-01",
            status=Event.CANCELLATION,
        )

        cls.response_hotel_1 = cls._create_response_dict(cls.event_1)
        cls.response_hotel_2 = cls._create_response_dict(cls.event_2)

        cls.path = reverse('event-list')

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)

    @staticmethod
    def _create_response_dict(event):
        return {
            "id": event.id,
            "hotel_id": event.hotel_id,
            "timestamp": event.event_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "rpg_status": event.status,
            "room_id": event.room_reservation_id,
            "night_of_stay": event.night_of_stay,
        }

    def _get_with_token(self, token):
        self.client.logout()
        return self.client.get(self.path, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})

    def _assert_response(self, response, expected_data):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], expected_data)

    def test_get_hotel_list_with_valid_token(self):
        """Test getting the hotel list with a valid access token."""
        response = self._get_with_token(AccessToken.for_user(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_hotel_list_with_invalid_token(self):
        """Test getting the hotel list with an invalid access token."""
        response = self._get_with_token(uuid4())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_hotel_list(self):
        """Test getting the hotel list."""
        response = self.client.get(self.path)
        self._assert_response(response, [self.response_hotel_1, self.response_hotel_2])

    def test_filter_hotel_list_by_hotel_id(self):
        """Test filtering the hotel list by hotel ID."""
        response = self.client.get(self.path, {"hotel_id": self.event_2.hotel_id})
        self._assert_response(response, [self.response_hotel_2])

    def test_filter_hotel_list_by_night_of_stay_date(self):
        """Test filtering the hotel list by night of stay date."""
        response = self.client.get(self.path, {"night_of_stay__gte": "2022-05-01"})
        self._assert_response(response, [self.response_hotel_2])

    def test_filter_hotel_list_by_room_id(self):
        """Test filtering the hotel list by room ID."""
        response = self.client.get(self.path, {"room_id": self.event_1.room_reservation_id})
        self._assert_response(response, [self.response_hotel_1])

    def test_filter_hotel_list_by_updated_date(self):
        """Test filtering the hotel list by updated date."""
        response = self.client.get(self.path, {"updated__gte": self.event_2.event_timestamp})
        self._assert_response(response, [self.response_hotel_2])

    def test_filter_hotel_list_by_rpg_status(self):
        """Test filtering the hotel list by RPG status."""
        response = self.client.get(self.path, {"rpg_status": Event.BOOKING})
        self._assert_response(response, [self.response_hotel_1])

    def test_create_event(self):
        """Test creating a new event."""
        data = {
            "room_id": self.event_1.room_reservation_id,
            "night_of_stay": self.event_1.night_of_stay,
            "rpg_status": Event.CANCELLATION,
            "hotel_id": self.event_1.hotel_id,
        }

        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Event.objects.filter(room_reservation_id=data["room_id"]).exists())
