"""Mission Control views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Rover, BlockDiagram
from rest_framework.renderers import JSONRenderer
from .serializers import BlockDiagramSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from .forms import RoverForm
from oauth2_provider.models import Application


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
def rover_settings(request, pk=None):
    """Rover settings view for the specific rover."""
    if pk:
        rover = get_object_or_404(Rover, owner=request.user, pk=pk)
    else:
        rover = Rover(owner=request.user)
    if request.method == 'POST':
        form = RoverForm(instance=rover, data=request.POST)

        if form.is_valid():
            form.save()
            if not rover.oauth_application:
                rover.oauth_application = _create_app(
                    request.user,
                    rover.name
                )
            rover.save()

    form = RoverForm(instance=rover)

    oa = rover.oauth_application
    return render(request, 'rover_settings.html', {
        'name': rover.name,
        'client_id': oa.client_id if oa else "",
        'client_secret': oa.client_secret if oa else "",
        'form': form
    })


def _create_app(user, name):
    return Application.objects.create(
        user=user,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        client_type=Application.CLIENT_CONFIDENTIAL,
        name=name
    )
