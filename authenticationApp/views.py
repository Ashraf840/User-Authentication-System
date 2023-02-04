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



class UserView(APIView):
    """
    User detail view API. Required authentication.
    """
    def get(self, request):
        token = request.COOKIES.get('jwt')   # Get the jwt token from cookies
        # check: token is not set/found
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        #decode the JWT token in order to get the payload
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")
        # fetch the user from db using the payload's key-value pair
        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)   # pass the user instance to get JSON serializable object
        return Response({
            'token': token,
            'user': serializer.data     # pass serialized object of user-model-instance, otherwise this API throws error if passed model-instance directly as response
        })
