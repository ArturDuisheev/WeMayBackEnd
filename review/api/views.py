from django.shortcuts import render


from rest_framework import generics, response, status, permissions

from review.models import Review
from .serializers import ReviewSerializer


class ReviewListAPIVIew(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]


# Create your views here.
