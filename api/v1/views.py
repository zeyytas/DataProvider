from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import EventSerializer
from event.filters import CustomEventFilter
from event.models import Event


class EventViewSet(ModelViewSet):
    """
    ViewSet for managing Event objects.
    """
    queryset = Event.objects.all().order_by("event_timestamp")
    pagination_class = PageNumberPagination
    serializer_class = EventSerializer
    filterset_class = CustomEventFilter
    permission_classes = [IsAuthenticated]
