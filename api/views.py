import rest_framework.permissions as perm
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Chapter, Comment, CommentResponse, Novel, Profile
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
            user = User(username=data.get("username"), email=data.get("email"))
            user.set_password(request.data.get("password"))
            user.save()
            return Response({"token": str(user.auth_token)})

    @action(detail=False, methods=["post"])
    def login(self, request):
        data = request.data
        user = authenticate(
            request, username=data["username"], password=data["password"]
        )
        if user:
            return Response({"token": str(user.auth_token)})
        return Response(
            {"details": "User not found, please register to get authenticated!"}
        )


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [perm.IsAuthenticated]
