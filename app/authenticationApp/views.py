from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.renderers import JSONRenderer     # Currently not using, since a custom renderer_class will be build later

class UserRegistration(APIView):
    # Choose a renderer class for this particular APIView
    # renderer_classes = [JSONRenderer]   # Options: JSONRenderer; Negate this LOC
    def post(self, request, format=None):
        return Response({'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
