from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Rover, BlockDiagram
from rest_framework import filters, viewsets
from rest_framework.response import Response
from .serializers import RoverSerializer, BlockDiagramSerializer
from mission_control.utils import remove_old_rovers
from datetime import timedelta


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

    def list(self, request):
        remove_old_rovers(timedelta(seconds=-5))
        queryset = Rover.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class BlockDiagramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows block diagrams to be viewed or edited.
    """
    queryset = BlockDiagram.objects.all()
    serializer_class = BlockDiagramSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user',)
