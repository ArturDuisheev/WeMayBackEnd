from django.urls import path
from .api.views import ReviewListCreateAPIVIew, MyReviewListAPIVIew, ReviewDetailAPIView, LikeCounterView

urlpatterns = [
    path('all/', ReviewListCreateAPIVIew.as_view()),
    path('my/', MyReviewListAPIVIew.as_view()),
    path('<int:pk>/', ReviewDetailAPIView.as_view()),
    path('<int:pk>/like/', LikeCounterView.as_view())
]
