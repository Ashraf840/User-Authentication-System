from django.urls import path
from .views import (
    RegisterUserAPI
    , VerifyUserEmailAPI
    , LoginUserAPI
    , TestAuthenticationAPI
    , PasswordResetRequestAPI
    , PasswordResetConfirmAPI
    , SetNewPasswordAPI
    , LogoutUserAPI
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterUserAPI.as_view(), name="RegisterUserAPI"),
    path('verify-email/', VerifyUserEmailAPI.as_view(), name="VerifyUserEmailAPI"),
    path('login/', LoginUserAPI.as_view(), name="LoginUserAPI"),
    path('refresh-token/', TokenRefreshView.as_view(), name="TokenRefreshView"),
    path('profile/', TestAuthenticationAPI.as_view(), name="TestAuthenticationAPI"),
    path('password-reset/', PasswordResetRequestAPI.as_view(), name="PasswordResetRequestAPI"),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmAPI.as_view(), name="PasswordResetConfirmAPI"),
    path('set-new-password/', SetNewPasswordAPI.as_view(), name="SetNewPasswordAPI"),
    path('logout/', LogoutUserAPI.as_view(), name="LogoutUserAPI"),
]

