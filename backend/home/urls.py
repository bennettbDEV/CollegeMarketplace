#home/urls.py
from django.urls import path
from . import views



urlpatterns = [
    path('', views.to_homepage, name='home'),  # The main homepage
]