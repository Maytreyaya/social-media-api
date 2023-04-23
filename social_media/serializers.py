
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserProfile, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "username", "email", )


class UserProfileSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    user = serializers.CharField(source="user.email", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    def get_following_count(self, obj):
        return obj.followers.count()

    class Meta:
        model = UserProfile
        fields = ("id", "user",
                  "bio",
                  "following_count",
                  "image", "username",)
        read_only_fields = ["id"]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    liked_posts = serializers.CharField(source="user.likes", read_only=True)

    def get_following(self, obj):
        following = obj.followers.all()
        return [follower.username for follower in following]

    def get_followers(self, obj):
        followers = obj.user.following.all()
        return [followed_user.user.username for followed_user in followers]

    class Meta:
        model = UserProfile
        fields = ("id",
                  "user",
                  "bio",
                  "username",
                  "image",
                  "followers",
                  "following",
                  "liked_posts")
        read_only_fields = ["id",]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "description", "created_at", "likes")
        read_only_fields = ["id", "created_by", "created_at"]


class PostListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title",
                  "description",
                  "created_by",
                  "created_at",
                  "likes"]
        read_only_fields = ["id",
                            "title",
                            "description",
                            "created_by",
                            "created_at",
                            "comments",
                            "likes"]


