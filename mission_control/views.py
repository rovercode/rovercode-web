from django.shortcuts import render
from .models import Rover
from rest_framework import viewsets
from .serializers import RoverSerializer

def home(request):
    return render(request, 'home.html')

class RoverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rovers to be viewed or edited.
    """
    queryset = Rover.objects.all()
    serializer_class = RoverSerializer
