from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


class RegisterView(APIView):
    """
    User registration API
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    """
    Login API to authenticate user using JWT authentication method.
    """
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        # check: incorrect email input
        if user is None:
            raise AuthenticationFailed('Authentication failed')
        # check: incorrect password input
        if not user.check_password(password):
            raise AuthenticationFailed("Authentication failed")

        # When successful, generate jwt
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),     # inteded to make token-expiry duration 60 mins from creation
            'iat': datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)  # Enabling the HTTPOnly attribute prevents malicious scripts from stealing the user's session identity. Prohibit the frontend to access the token.
        response.data = {
            'jwt': token
        }
        return response
