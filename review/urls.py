from django.urls import path
from .api.views import ReviewListAPIVIew

urlpatterns = [
    path('review/', ReviewListAPIVIew.as_view())
]
