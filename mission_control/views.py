from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Rover, BlockDiagram
from rest_framework import filters, viewsets
from .serializers import RoverSerializer, BlockDiagramSerializer


def home(request):
    return render(request, 'home.html')


@login_required
def list(request):
    bd_list = BlockDiagram.objects.filter(user=request.user.id)
    return render(request, 'list.html', {'bd_list': bd_list})


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
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user',)
