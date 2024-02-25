from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer, RequetNewOTPSerializer, UserLoginSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer, LogoutUserSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import OneTimePassword
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User


class APIEndpointDoc(GenericAPIView):
    def get(self, request):
        return Response({
            'User Registration':'api/v1/auth/register/',
            'Email Verification':'api/v1/auth/verify-email/',
            'User Login':'api/v1/auth/login/',
            'User Profile':'api/v1/auth/profile/',
            'Password Reset Request':'api/v1/auth/password-reset/',
            'Password Reset Confirm':'api/v1/auth/password-reset-confirm/<user_id>/<pass-reset-token>/',
            'Set New Password':'api/v1/auth/set-new-password/',
            'User Logout':'api/v1/auth/logout/',
            'Refresh Token':'api/v1/auth/refresh-token/',
        }, status=status.HTTP_200_OK)


class RegisterUserAPI(GenericAPIView):
    serializer_class=UserRegisterSerializer

    def post(self, request):
        user_data=request.data
        serializer=self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            # Send email to the the user's email address
            send_code_to_user(user['email'])
            return Response({
                'data':user,
                'message':f"hi {user['first_name']}, your registration is successful"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestNewOTPAPI(GenericAPIView):
    serializer_class=RequetNewOTPSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            result=send_code_to_user(email=serializer.data.get('email'), repeat_otp_code=True)
            if result:
                return Response(data={"message":"Failed to send OTP code"}, status=status.HTTP_200_OK)
            return Response(data={"message":"A new OTP code is sent to your email"}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmailAPI(GenericAPIView):
    def post(self, request):
        otp_code=request.data.get('otp', None)    # Default value: None
        try:
            user_code=OneTimePassword.objects.get(code=otp_code)
            user=user_code.user
            # Check user is verified, make verified otherwise
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({
                    'message':'Account email verified successfully'
                }, status=status.HTTP_200_OK)
            else:
                # TODO: Add a new api endpoint which generate OTP code for email verfication for the user (get a track for requesting (max 3, then the account will be banned) to mail-verfication after failing to verify email after registering into the system)
                return Response({
                    'message':'Invalid code, account is already verified'
                }, status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            # If the OTP code is not sent through POST method or, the code does not exist in the db, then this exception block will be executed
            return Response({
                'message':'OTP not provided'
            }, status=status.HTTP_404_NOT_FOUND)


class LoginUserAPI(GenericAPIView):
    serializer_class=UserLoginSerializer
    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestAuthenticationAPI(GenericAPIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        data={
            'message':'It works'
        }
        return Response(data, status=status.HTTP_200_OK)


class PasswordResetRequestAPI(GenericAPIView):
    serializer_class=PasswordResetRequestSerializer
    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({
            'message':'A link has been sent to your mailbox to reset your password'
        }, status=status.HTTP_200_OK)
    

class PasswordResetConfirmAPI(GenericAPIView):
    # User will click the link (frontend-app-view), which will make a GET request to this API before redirecting the user to password reset form
    # Controls the frontend web part whether to show error-msg-page or pass-reset-form
    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            # Check if a pass-reset-token is correct for a given user
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'message':'Token is invalid or has expired'
                }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'message':'Token is valid',
                'uidb64':uidb64,
                'token':token,
            }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({
                'message':'Token is invalid or has expired'
            }, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPI(GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'message':'Password reset successfully'
        }, status=status.HTTP_200_OK)


class LogoutUserAPI(GenericAPIView):
    # In frontend, clear the state of the "access_token" & blacklist the "refresh_token" in the backend
    serializer_class=LogoutUserSerializer
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message':'User logged out'
        }, status=status.HTTP_205_RESET_CONTENT)
