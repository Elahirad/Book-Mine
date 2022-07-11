from django.shortcuts import render
from rest_framework.views import APIView, Response

class HelloWorldView(APIView):
    def get(self, request):
        return Response({"result": "OK"})
