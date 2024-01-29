from django.urls import path
from .api.views import ReviewListCreateAPIVIew, ReviewDetailAPIView, LikeCounterView

urlpatterns = [
    path('review/', ReviewListCreateAPIVIew.as_view()),
    path('review/<int:pk>', ReviewDetailAPIView.as_view()),
    path('review/<int:pk>/like', LikeCounterView.as_view())
]
