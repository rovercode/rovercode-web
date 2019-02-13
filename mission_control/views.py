"""Mission Control views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.renderers import JSONRenderer

from .models import BlockDiagram
from .serializers import BlockDiagramSerializer


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
    bds = BlockDiagram.objects.filter(user=request.user.id)
    return render(request, 'bd_list.html', {'bd_list': bds})
