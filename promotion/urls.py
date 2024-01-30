from django.urls import path
from .api import views

urlpatterns = [
    path('category/all/', views.PromotionCategoryListCreateAPIView.as_view(), name='category'),
    path('category/<int:id>/', views.PromotionCategoryDetailAPIView.as_view(), name='category-detail'),
    path('category/<int:id>/promotion/all/', views.PromotionListAPIView.as_view(), name='promotion'),
    path('category/<int:id>/promotion/<int:pk>/', views.PromotionDetailAPIView.as_view(), name='promotion-detail'),
    path('category/<int:id>/promotion/<int:pk>/like/', views.LikeCounterView.as_view(), name='like-counter'),
]
