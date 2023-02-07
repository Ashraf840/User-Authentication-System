from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class IndexView(APIView):
    """
    Public API for welcome page
    """

    def get(self, request, format=None):
        content = {
            'wmsg': 'Welcome to full stack development',
        }
        return Response(content)
