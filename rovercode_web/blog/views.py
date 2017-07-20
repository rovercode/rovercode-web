"""Blog views."""
from django.shortcuts import render

def list(request):
    """Test view."""
    return render(request, 'list.html')
