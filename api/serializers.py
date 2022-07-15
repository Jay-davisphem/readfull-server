from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Chapter, Comment, CommentResponse, Novel, Profile


class UserSerializer(serializers.ModelSerializer):
    profile_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "profile_id"]
        extra_kwargs = {"password": {"write_only": True}}

    def get_profile_id(self, obj):
        return obj.profile.pk


class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_profile_picture(self, obj):
        return obj.profile_picture.url

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["title", "content", "novel_id", "chapter_no"]


class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentResponse
        fields = "__all__"
