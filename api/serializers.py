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
    chapter_no = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ["title", "content", "novel_id", "chapter_no"]

    def get_chapter_no(self, obj):
        if isinstance(Chapter, obj):
            return obj.chapter_no
        return obj.get("chapter_no")


class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    which_comment = serializers.SerializerMethodField()
    from_ = serializers.PrimaryKeyRelatedField(source="commentor", read_only=True)
    novel = serializers.IntegerField(source="chapter.novel.pk")

    class Meta:
        model = Comment
        fields = ["id", "novel", "which_comment", "chapter", "from_", "message"]

    def get_which_comment(self, obj):
        if isinstance(obj, Comment):
            return f"{obj.chapter.novel.title} - chapter {obj.chapter.chapter_no} | comment {obj.chapter.id} by {obj.commentor.username}"


class CommentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentResponse
        fields = "__all__"
