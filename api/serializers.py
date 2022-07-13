from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Chapter, Comment, CommentResponse, Novel, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1

    def get_profile_picture(self, obj):
        return obj.profile_picture.url


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"


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
