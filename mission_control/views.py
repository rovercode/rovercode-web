"""Mission Control views."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .models import Rover, BlockDiagram
from rest_framework.renderers import JSONRenderer
from .serializers import BlockDiagramSerializer
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
