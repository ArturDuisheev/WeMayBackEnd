from django.urls import path
from .api.views import ReviewListAPIVIew

urlpatterns = [
    path('reviews/all/', ReviewListAPIVIew.as_view())
]
