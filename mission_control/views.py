from django.shortcuts import render

def home(request):
    return render(request, 'mission-control/home.html')
