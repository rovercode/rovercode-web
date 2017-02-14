from django.shortcuts import render
from .models import Rover, BlockDiagram
from rest_framework import viewsets
from .serializers import RoverSerializer, BlockDiagramSerializer

def home(request):
    return render(request, 'home.html')

class RoverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rovers to be viewed or edited.
    """
    queryset = Rover.objects.all()
    serializer_class = RoverSerializer


class BlockDiagramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows block diagrams to be viewed or edited.
    """
    queryset = BlockDiagram.objects.all()
    serializer_class = BlockDiagramSerializer
