#home/views
from django.shortcuts import render



def index(request):
    # This is where you can fetch featured products or any other initial data to display
    return render(request, 'index.html',{})