#backend/urls
#This is the central point for all URLs so far

"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import LoginView

urlpatterns = [
    #CHASE ADDITIONS
    path('', include('home.urls')),  #Central home page

    path('admin/', admin.site.urls),
    # Authentication
    # api/token/ is used for logging in, token/refresh/ is used to refresh access token
    path("api/token/", LoginView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),

    # Main api urls
    path("api/", include("api.urls")),
]
