from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import docs_urls, views

login = views.UserViewSet.as_view({"post": "login"})
register = views.UserViewSet.as_view({"post": "register"})

router = DefaultRouter()
router.register(r"profiles", views.ProfileViewSet, basename="profiles")
router.register("novels", views.NovelViewSet, basename="novels")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
]

urlpatterns += docs_urls.urlpatterns
