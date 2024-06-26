from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.v1.urls import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls), name="event"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
