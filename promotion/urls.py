from django.urls import path
from promotion.api.views import PromotionCategoryListAPIView, PromotionCategoryDetailAPIView, PromotionListAPIView, PromotionDetailAPIView, LikeCounterView
urlpatterns = [
    path('category/all/', PromotionCategoryListAPIView.as_view(), name='category'),
    path('category/<int:id>/', PromotionCategoryDetailAPIView.as_view(), name='category-detail'),
    path('category/<int:id>/promotion/', PromotionListAPIView.as_view(), name='promotion'),
    path('category/<int:id>/promotion/<int:pk>/', PromotionDetailAPIView.as_view(), name='promotion-detail'),
    path('category/<int:id>/promotion/<int:pk>/like/', LikeCounterView.as_view(), name='like-counter'),
]
