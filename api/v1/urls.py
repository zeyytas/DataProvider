from rest_framework import routers

from api.v1.views import EventViewSet

router = routers.DefaultRouter()

router.register(r'events', EventViewSet)
