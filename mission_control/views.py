"""Mission Control views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import Rover, BlockDiagram
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import RoverSerializer, BlockDiagramSerializer
from mission_control.utils import remove_old_rovers
from datetime import timedelta
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def home(request):
    """Home view."""
    return render(request, 'home.html')


@login_required
def list(request):
    """Block diagram list view for the logged in user."""
    bd_list = BlockDiagram.objects.filter(user=request.user.id)
    return render(request, 'list.html', {'bd_list': bd_list})


class RoverViewSet(viewsets.ModelViewSet):
    """API endpoint that allows rovers to be viewed or edited."""

    queryset = Rover.objects.all()
    serializer_class = RoverSerializer

    def list(self, request):
        """Remove old rovers and lists the remaining active rovers."""
        remove_old_rovers(timedelta(seconds=-5))
        queryset = Rover.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BlockDiagramViewSet(viewsets.ModelViewSet):
    """API endpoint that allows block diagrams to be viewed or edited."""

    queryset = BlockDiagram.objects.all()
    serializer_class = BlockDiagramSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user','name')
