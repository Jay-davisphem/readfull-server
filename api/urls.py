from django.urls import include, path

from . import docs_urls, views

# from rest_framework.authtoken import views as authviews
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"users", views.UserViewSet, basename="users")
# router.register(r"profiles", views.ProfileViewSet, basename="profiles")

login = views.UserViewSet.as_view({"post": "login"})
register = views.UserViewSet.as_view({"post": "register"})
urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
]

urlpatterns += docs_urls.urlpatterns
