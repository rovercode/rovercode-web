from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import Rover
from rest_framework import viewsets
from .serializers import RoverSerializer

def home(request):
    return render(request, 'home.html')

class RoverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Rover.objects.all()
    serializer_class = RoverSerializer
