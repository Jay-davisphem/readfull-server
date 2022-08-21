from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Chapter, Comment, CommentResponse, Follower, Following,
                     Novel, Profile)
from .permissions import (IsAuthorOrAdmin, IsCommenterOrAdmin,
                          IsNovelistOrAdmin, IsOwnerOrAdmin,
                          IsResponderOrAdmin)
from .serializers import (ChapterSerializer, CommentResponseSerializer,
                          CommentSerializer, NovelSerializer,
                          ProfileSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["post"])
    def register(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            user = User(username=data.get("username"))
            if data.get("email"):
                user.email = data.get("email")
            user.set_password(request.data.get("password"))
            user.save()

            data["email"] = user.email
            data["profile_id"] = user.profile.pk
            return Response(
                {
                    "token": str(user.auth_token),
                    "user": data,
                }
            )

    @action(detail=False, methods=["post"])
    def login(self, request):
        data = request.data
        user = authenticate(
            request, username=data["username"], password=data["password"]
        )

        if user:
            data = UserSerializer(data).data
            data["email"] = user.email
            data["profile_id"] = user.profile.pk
            return Response({"token": str(user.auth_token), "user": data})

        return Response(
            {
                "details": "User not found, \
             please register to get authenticated!"
            }
        )


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrAdmin]

    @action(detail=True, methods=["put", "post", "patch"])
    def follow(self, request, pk=None):
        flw = get_object_or_404(self.get_queryset(), pk=pk)
        user = request.user
        try:
            flr, __ = Follower.objects.get_or_create(user=user.profile)
            fln, _ = Following.objects.get_or_create(user=flw)
            flw.followers.add(flr)
            user.profile.followings.add(fln)
            return Response({"detail": f"{request.user} followed {flw.user}"})
        except Exception as e:
            return Response(
                {"detail": f"Internal server error ------> \n{e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["put", "post", "patch"])
    def unfollow(self, request, pk=None):
        fin = get_object_or_404(self.get_queryset(), pk=pk)
        user = request.user
        try:
            fin.followers.remove(user.profile)
            user.profile.followings.remove(pk)
            return Response(
                {
                    "detail": f"{request.user} unfollowed {fin.user}",
                }
            )
        except Exception:
            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NovelViewSet(viewsets.ModelViewSet):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer
    permission_classes = [IsAuthorOrAdmin]

    def create(self, request):
        user_id = request.user.id
        data = request.data
        serializer = NovelSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author_id=user_id)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Novel, pk=pk)
        obj.view_count += 1
        obj.save()

        return super().retrieve(request)


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsNovelistOrAdmin]

    def get_novel(self, pk=None):
        return get_object_or_404(Novel, pk=pk)

    def get_object(self, pk=None, ch_pk=None):
        return get_object_or_404(
            self.get_queryset().filter(novel_id=pk), chapter_no=ch_pk
        )

    def create(self, request, pk=None):
        novel = self.get_novel(pk)
        last = novel.chapter_set.last()
        serializer = ChapterSerializer(request.data)
        data = serializer.data
        if last:
            ch = Chapter.objects.create(
                **{**data, "novel_id": pk, "chapter_no": last.chapter_no + 1}
            )
        else:
            ch = Chapter.objects.create(
                title=data["title"], content=data["content"], novel_id=pk, chapter_no=1
            )
        serializer = ChapterSerializer(ch)
        return Response(
            {
                "details": f"{novel.title}\
 Chapter {ch.chapter_no} successfully created",
            },
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None, ch_pk=None):
        self.get_novel(pk)
        ch = self.get_object(pk=pk, ch_pk=ch_pk)
        serializer = ChapterSerializer(ch)
        return Response(serializer.data)

    def list(self, request, pk=None):
        self.get_novel(pk)
        chs = Chapter.objects.filter(novel_id=pk)
        page = self.paginate_queryset(chs)
        if page:
            print(f"{page=}")
            data = ChapterSerializer(page, many=True).data
            return self.get_paginated_response(data)
        data = ChapterSerializer(chs, many=True).data
        return Response(data)

    def __detail(self, request, pk=None, ch_pk=None):
        self.get_novel(pk=pk)
        return self.get_object(pk=pk, ch_pk=ch_pk)

    def destroy(self, request, pk=None, ch_pk=None):
        self.__detail(request, pk, ch_pk).delete()
        return Response("Deleted successfully")

    def update(self, request, pk=None, ch_pk=None):
        ch = self.__detail(request, pk, ch_pk)
        data = ChapterSerializer(request.data).data
        p_title = ch.title
        p_content = ch.content
        p_chn = ch.chapter_no

        try:
            ch.title = data.get("title", p_title)
            ch.content = data.get("content", p_content)
            ch.chapter_no = request.data.get("chapter_no", p_chn)
            ch.save()
            data = ChapterSerializer(ch).data
            return Response(data)
        except Exception:
            return Response("Could not update {ch.title}")


viewsets.ViewSet


class GenreAPIView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            genres = Novel.GENRE_CHOICES
            return Response(genres)
        else:
            return Response(
                {"details": "Not authenticated!"},
                status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
            )


class StatusAPIView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            statuses = Novel.NovelStatus.choices
            return Response(statuses)
        else:
            return Response(
                {"details": "Not authenticated!"},
                status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
            )


class LikesAPIView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            likes = Chapter.LikesChoices.choices
            return Response(likes)
        else:
            return Response(
                {"details": "Not authenticated!"},
                status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
            )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommenterOrAdmin]

    def create(self, request, *args):
        data = request.data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True) and data.get("chapter"):
            serializer.save(commentor=request.user)
            return Response(serializer.data)


class CommentResponseViewSet(viewsets.ModelViewSet):
    queryset = CommentResponse.objects.all()
    serializer_class = CommentResponseSerializer
    permission_classes = [IsResponderOrAdmin]
