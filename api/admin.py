from django.contrib import admin

from .models import Chapter, Comment, CommentResponse, Novel, Profile

admin.site.register(Profile)
admin.site.register(Novel)
admin.site.register(Chapter)
admin.site.register(Comment)
admin.site.register(CommentResponse)
