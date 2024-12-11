# api/urls.py

import user_messages.views as message_views
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
import api.views as views

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

# Setup Variables
router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"listings", views.ListingViewSet, basename="listing")
router.register(r"messages", message_views.MessageViewSet, basename="message")
""" The router creates the following urlpatterns + any extra actions defined in the view:
- listings/,  name='listing-list'
- listings/<int:pk>/, name='listing-detail'
- users/,  name='user-list'
- users/<int:pk>/, name='user-detail'
"""

urlpatterns = [
    path("", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("", include(router.urls)),
]