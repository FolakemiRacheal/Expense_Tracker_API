from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomRegisterView, UserProfileView, CustomTokenObtainPairView


app_name = "ums"
router = DefaultRouter()



urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("", include(router.urls)),
]
