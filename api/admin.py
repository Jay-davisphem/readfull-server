from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Chapter, Comment, CommentResponse, Follower, Following,
                     Like, Novel, Profile, User)


class NovelInline(admin.StackedInline):
    model = Novel


class ChapterInline(admin.TabularInline):
    model = Chapter


class CommentInline(admin.TabularInline):
    model = Comment


class ResponseInline(admin.TabularInline):
    model = CommentResponse


class UserAdmin(UserAdmin):
    inlines = [NovelInline]
    extra = 0


class FollowerInline(admin.TabularInline):
    model = Follower
    fk_name = "who"


class FollowingInline(admin.TabularInline):
    model = Following
    fk_name = "who"


class ProfileAdmin(admin.ModelAdmin):
    inlines = [FollowerInline, FollowingInline]


admin.site.unregister(User)

admin.site.register(Novel)
admin.site.register(Chapter)
admin.site.register(Follower)
admin.site.register(Following)
admin.site.register(Comment)
admin.site.register(CommentResponse)
admin.site.register(Like)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
