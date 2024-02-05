from django.urls import path
from .api import views

urlpatterns = [
    path('all/', views.ReviewListAPIVIew.as_view()),
    path('all/<str:my>', views.ReviewListAPIVIew.as_view()),
    path('create/', views.ReviewCreateAPIVIew.as_view()),
    path('<int:pk>/', views.ReviewDetailAPIView.as_view()),
    path('<int:pk>/like/', views.LikeCounterView.as_view()),
]
