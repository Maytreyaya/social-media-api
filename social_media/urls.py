from django.urls import path, include
from rest_framework import routers

from social_media.views import ProfileViewSet

router = routers.DefaultRouter()
router.register("profile", ProfileViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "social_media"

