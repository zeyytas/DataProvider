import json
import logging
import uuid
from random import randint

import requests
from celery import shared_task
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger(__name__)


def create_random_event_data() -> dict:
    """
    Generate random event data for simulating event creation.

    Returns:
        dict: Randomly generated event data.
    """
    random_data = {
        "room_id": str(uuid.uuid4()),
        "night_of_stay": f"2025-{randint(1, 12):02d}-{randint(1, 28):02d}",
        "rpg_status": randint(1, 2),
        "hotel_id": randint(1, 3000),
    }
    return random_data


def generate_jwt_token() -> str:
    """
    Generate a JWT token for authentication.

    Returns:
        str: JWT token string.
    """
    user = User.objects.first()  # Which is created here event/migrations/0003_create_user.py
    token = AccessToken.for_user(user)
    return str(token)


def send_data_to_api(data):
    """
    Send event data to the API endpoint.

    Args:
        data (dict): Event data to be sent to the API.

    Returns:
        requests.Response: Response object from the API.
    """
    event_url = "http://web:8000" + reverse("event-list")
    access_token = generate_jwt_token()
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    response = requests.post(event_url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response


@shared_task
def create_events():
    """
    Task to create events by sending data to the API endpoint.

    Raises:
        Exception: If an error occurs during event creation.
    """
    try:
        logger.info("START: Creating event object")
        data = create_random_event_data()
        response = send_data_to_api(data)
        logger.info(f"FINISH: Event object created successfully. Response: {response.status_code}")

    except Exception as e:
        logger.error(f"An error occurred during event creation: {str(e)}")
