from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("user-detail/", UserView.as_view(), name='userDetail'),
]