#home/views
from django.shortcuts import render



def to_homepage(request):
    # This is where you can fetch featured products or any other initial data to display
    return render(request, 'home/homepage.html',{})