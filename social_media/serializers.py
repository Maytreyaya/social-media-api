from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()

    def get_following_count(self, obj):
        return obj.followers.count()

    class Meta:
        model = UserProfile
        fields = ["id", "user", "followers", "following_count"]
        read_only_fields = ["id", "user"]
