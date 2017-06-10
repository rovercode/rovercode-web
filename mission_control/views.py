"""Mission Control views."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from .models import Rover, BlockDiagram
from rest_framework import viewsets, permissions, serializers
from rest_framework.renderers import JSONRenderer
from .serializers import RoverSerializer, BlockDiagramSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from .forms import RoverForm


@ensure_csrf_cookie
def home(request, bd=None):
    """Home view."""
    if bd is not None:
        bd_object = get_object_or_404(BlockDiagram, id=bd)
        bd_data = BlockDiagramSerializer(bd_object).data
        bd_serial = JSONRenderer().render(bd_data)
    else:
        bd_serial = "None"
    return render(request, 'home.html', {'bd': bd_serial})


@login_required
def bd_list(request):
    """Block diagram list view for the logged in user."""
    bd_list = BlockDiagram.objects.filter(user=request.user.id)
    return render(request, 'bd_list.html', {'bd_list': bd_list})


@login_required
def rover_list(request):
    """Rover list view for the logged in user."""
    rover_list = Rover.objects.filter(owner=request.user.id)
    return render(request, 'rover_list.html', {'rover_list': rover_list})


@login_required
def rover_settings(request, pk):
    """Rover settings view for the specific rover."""
    rover = get_object_or_404(Rover, owner=request.user, pk=pk)
    print(request.POST)
    if request.method == 'POST':
        form = RoverForm(instance=rover, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('mission-control:rover_list'))

        form = RoverForm(instance=rover)
    else:
        form = RoverForm(instance=rover)

    return render(request, 'rover_settings.html', {
        'name': rover.name,
        'form': form
    })


class RoverViewSet(viewsets.ModelViewSet):
    """API endpoint that allows rovers to be viewed or edited."""

    serializer_class = RoverSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name',)

    def get_queryset(self):
        """The list of rovers for the user."""
        return Rover.objects.filter(owner=self.request.user.id)


class BlockDiagramViewSet(viewsets.ModelViewSet):
    """API endpoint that allows block diagrams to be viewed or edited."""

    queryset = BlockDiagram.objects.all()
    serializer_class = BlockDiagramSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'name')

    def perform_create(self, serializer):
        """Perform the create operation."""
        user = self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        """Perform the update operation."""
        if self.get_object().user.id is not self.request.user.id:
            raise serializers.ValidationError(
                'You may only modify your own block diagrams')
        serializer.save()
