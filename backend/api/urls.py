#api/urls.py
'''
EDIT_OUT:
(TO_CHANGE)
'''

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, ListingViewSet
from . import views
from . views import LoginView
from django.contrib.auth.views import LoginView #this can be changed if not needed TO_CHANGE

# Alternatively we can do
"""
listing_list = ListingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
listing_detail = ListingViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
with urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('listings/', listing_list, name='listing-list'),
    path('listings/<int:pk>/', listing_detail, name='listing-detail'),
"""

#Setup Variables
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"listings", ListingViewSet, basename="listing")
user_delete = UserViewSet.as_view({"delete": "destroy"})
""" The router creates the following urlpatterns:
- listings/,  name='listing-list'
- listings/<int:pk>/, name='listing-detail'
- users/,  name='user-list'
- users/<int:pk>/, name='user-detail'
"""


urlpatterns = [
    path('', views.to_homepage, name='home'),  # The main homepage
    #login (TO_CHANGE)
    path('login/', LoginView.as_view(template_name='api\login.html'), name='login'),
    path('', include(router.urls)),
    path("users/<int:pk>/delete/", user_delete, name="user-delete"),
]
