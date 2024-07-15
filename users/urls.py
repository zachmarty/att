from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import UsersViewSet


app_name = UsersConfig.name
router = DefaultRouter()
router.register(r"users", UsersViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls), name="users"),
    path("", include("djoser.urls.authtoken"))
]
