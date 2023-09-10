from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.renderers import JSONRenderer     # Currently not using, since a custom renderer_class will be build later
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from .renderers import JsonRenderer


class UserRegistration(APIView):
    # Choose a renderer class for this particular APIView
    # renderer_classes = [JSONRenderer]   # Options: JSONRenderer; Negate this LOC
    renderer_classes = [JsonRenderer]   # Custom render class
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
        # Provide a custom error msg using the key "non_field_errors"
        # return Response({"non_field_errors": "custom msg"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    renderer_classes = [JsonRenderer]   # Custom render class
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                return Response({'msg': 'Login successful'}, status=status.HTTP_200_OK)
            return Response({'errors': {'non_field_errors': 'Email or password is not valid'}}, status=status.HTTP_404_NOT_FOUND)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
