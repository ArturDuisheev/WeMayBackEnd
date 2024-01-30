from django.urls import path
from .api.views import ReviewListCreateAPIVIew, MyReviewListAPIVIew, ReviewDetailAPIView, LikeCounterView

urlpatterns = [
    path('review/all/', ReviewListCreateAPIVIew.as_view()),
    path('review/my/', MyReviewListAPIVIew.as_view()),
    path('review/<int:pk>/', ReviewDetailAPIView.as_view()),
    path('review/<int:pk>/like/', LikeCounterView.as_view())
]
