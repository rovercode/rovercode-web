from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import Rover

def home(request):
    return render(request, 'home.html')

# don't need in deployment, which uses HTTPS
@csrf_exempt
def rovers(request):
    if request.method == 'POST':
        rover = Rover()
        rover.name = request.POST['name']
        rover.owner = request.POST['owner']
        rover.local_ip = request.POST['local_ip']
        rover.last_checkin = timezone.now()
        return HttpResponse('')
    elif request.method == 'GET':
        print("Getting rovers")
        rovers = Rover.objects.all()
        response = serializers.serialize("json", rovers)
        return HttpResponse(response, content_type="application/json")
