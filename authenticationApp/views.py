from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed



class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
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

        return Response({
            "message": "Successful"
        })
