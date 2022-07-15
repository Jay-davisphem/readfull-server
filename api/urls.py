from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import docs_urls, views

login = views.UserViewSet.as_view({"post": "login"})
register = views.UserViewSet.as_view({"post": "register"})

router = DefaultRouter()
router.register(r"profiles", views.ProfileViewSet, basename="profiles")
router.register("novels", views.NovelViewSet, basename="novels")
chapter_list = views.ChapterViewSet.as_view({"post": "create", "get": "list"})
chapter_detail = views.ChapterViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)
urlpatterns = [
    path("", include(router.urls)),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("novels/<int:pk>/chapters/", chapter_list, name="chapter_list"),
    path(
        "novels/<int:pk>/chapters/<int:ch_pk>/", chapter_detail, name="chapter_detail"
    ),
]

urlpatterns += docs_urls.urlpatterns
