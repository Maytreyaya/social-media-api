from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_media.models import UserProfile, Post
from social_media.permissions import IsOwnerOrReadOnly
from social_media.serializers import (UserProfileSerializer,
                                      UserProfileDetailSerializer,
                                      PostSerializer,
                                      PostListSerializer)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.prefetch_related("followers").select_related("user")
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        username = self.request.query_params.get("username")

        queryset = self.queryset

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return UserProfileSerializer

        if self.action == "retrieve":
            return UserProfileDetailSerializer

        return UserProfileSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
    follow_u = get_object_or_404(get_user_model(), id=user_id)
    user_profile.followers.add(follow_u)
    return Response({'message': 'You are now following this user.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
    unfollow_u = get_object_or_404(get_user_model(), id=user_id)
    user_profile.followers.remove(unfollow_u)
    return Response({'message': 'You are not following this user.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostListSerializer

    def get_queryset(self):
        queryset = Post.objects.select_related("created_by").prefetch_related("liked_by")
        search = self.request.query_params.get("q")
        following = self.request.user.following.all()
        following_ids = following.values_list("user_id", flat=True)
        queryset = queryset.filter(Q(created_by=self.request.user) | Q(created_by__in=following_ids))

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        return queryset

    def perform_destroy(self, instance):
        if instance.created_by == self.request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "q",
                type=OpenApiTypes.STR,
                description="Filter by post title or description (ex. ?q=how)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.liked_by.add(request.user)
    return Response({'message': 'Post liked.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.liked_by.remove(request.user)
    return Response({'message': 'Post unliked.'})
