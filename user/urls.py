from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views


app_name = "user"


urlpatterns = [
    path("register/", views.UserRegisterationAPIView.as_view(), name="REGISTER"),
    path("login/", views.UserLoginAPIView.as_view(), name="LOGIN"),
    path("token/refresh/", TokenRefreshView.as_view(), name="REFRESH-TOKEN"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="LOGOUT"),
    path("", views.UserAPIView.as_view(), name="USER"),
]
