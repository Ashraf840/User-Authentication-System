from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.renderers import JSONRenderer     # Currently not using, since a custom renderer_class will be build later
from .serializers import UserRegistrationSerializer

class UserRegistration(APIView):
    # Choose a renderer class for this particular APIView
    # renderer_classes = [JSONRenderer]   # Options: JSONRenderer; Negate this LOC
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
        # Provide a custom error msg using the key "non_field_errors"
        # return Response({"non_field_errors": "custom msg"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
