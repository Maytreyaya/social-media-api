from django.urls import path, include
from rest_framework import routers

from social_media.views import (ProfileViewSet,
                                follow_user,
                                unfollow_user,
                                upload_post,
                                PostViewSet,
                                like_post,
                                unlike_post)

router = routers.DefaultRouter()
router.register("accounts", ProfileViewSet, basename="accounts")
router.register("posts", PostViewSet, basename="posts")


urlpatterns = [
    path("", include(router.urls)),
    path("follow/<int:user_id>/", follow_user, name="follow"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow"),
    path("create_post/", upload_post, name="create-post"),
    path("like/<int:post_id>/", like_post, name="like"),
    path("unlike/<int:post_id>/", unlike_post, name="unlike"),
]

app_name = "social_media"

