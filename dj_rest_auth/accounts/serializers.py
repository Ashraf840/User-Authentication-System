from tokenize import TokenError
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt_blacklist.tokens import RefreshToken
# from rest_framework_simplejwt.models import OutstandingToken



class UserRegisterSerializer(serializers.ModelSerializer):
    # "password" & "password2" are defined in an abstract manner in the "User" model.
    # The "write_only=True" param ensures that the serializer won't show while serializing the representation
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2=serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=User
        fields=['email', 'first_name', 'last_name', 'password', 'password2']
    
    def validate(self, attrs):
        """This method gets invoked when the "is_valid() method is called"""
        # Validate "password" & "password2" has the same value
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Password do not match")
        return attrs    # return the attributes if password matched

    def create(self, validated_data):
        """This method gets invoked when the "save()" method is called"""
        user=User.objects.create_user(
            email=validated_data.get('email')
            , first_name=validated_data.get('first_name')
            , last_name=validated_data.get('last_name')
            , password=validated_data.get('password')
        )
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    # The "read_only=True" param ensures that the field(s) will be used while serializing the representation, but not used while creating or updating an instance during deserializing
    email=serializers.EmailField(max_length=255, min_length=6)
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    full_name=serializers.CharField(max_length=255, read_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model=User
        fields=['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        request=self.context.get('request')
        user=authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials", 401)
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified", 401)
        user_tokens=user.tokens()   # Generate new pair of access & refresh token
        return {
            'email':user.email,
            'full_name':user.get_full_name,
            'access_token': user_tokens.get('access'),
            'refresh_token': user_tokens.get('refresh'),
        }


class PasswordResetRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)

    class Meta:
        fields=['email']
    
    def validate(self, attrs):
        email=attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("No account found", 404)
        else:
            user=User.objects.get(email=email)
            # Check if the user is already verified before proceed further. Otherwise raise validationError
            if not user.is_verified:
                raise serializers.ValidationError("Email is not verified", 401)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            # Get the domain of the frontend app (Majorly required if hosted separately)
            site_domain=get_current_site(request).domain
            relative_link=reverse('PasswordResetConfirmAPI', kwargs={'uidb64':uidb64, 'token':token}) # Another view/api, where the user will be redirected; This "PasswordResetConfirmAPI" value came from the 'name' param of the urlpatterns
            abslink=f"http://{site_domain}{relative_link}"
            email_body=f"Hi, use the link below to reset your password \n {abslink}"
            data={
                'email_body':email_body,
                'email_subject':'Reset you password',
                'to_email':user.email
            }
            # print("Email body data:", data)
            # Send email to user mailbox
            send_normal_email(data)

        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields=['password', 'confirm_password', 'uidb64', 'token']
    
    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Token is invalid or has expired', 401)
            if password != confirm_password:
                raise AuthenticationFailed('Password do not matched', 400)
            # Check if the new provided password is similar to the old password
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('Token is invalid or has expired', 401)


class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_message={
        'bad_token':{"Token is invalid or has expired"}
    }

    def validate(self, attrs):
        self.token=attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
