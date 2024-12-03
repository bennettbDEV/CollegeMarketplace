#api/urls.py
'''
EDIT_OUT:
(TO_CHANGE)
'''

from django.urls import include, path
from rest_framework.routers import DefaultRouter

import api.views as views
import user_messages.views as message_views
from . views import LoginView

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
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"listings", views.ListingViewSet, basename="listing")
router.register(r"messages", message_views.MessageViewSet, basename="message")
""" The router creates the following urlpatterns:
- listings/,  name='listing-list'
- listings/<int:pk>/, name='listing-detail'
- users/,  name='user-list'
- users/<int:pk>/, name='user-detail'
"""

urlpatterns = [
    path('', views.to_homepage, name='home'),  #the main homepage
    #path('login/', LoginView.as_view(template_name='api\login.html'), name='login'),
    path('', include(router.urls)),
]
