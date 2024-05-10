from django.urls import path
from .api import views

urlpatterns = [
    path('category/create/', views.PromotionCategoryCreateAPIView.as_view(), name='category-create'),
    path('category/all/', views.PromotionCategoryListAPIView.as_view(), name='category'),
    path('category/<int:pk>/', views.PromotionCategoryDetailAPIView.as_view(), name='category-detail'),
    path('contact/add/', views.PromotionContactCreateAPIView.as_view(), name='promotion-contact-create'),
    # Path filter (free, end_soon, daily, liked) are used to filter the objects by these fields
    path('all/<str:filter>/', views.PromotionListAPIView.as_view(), name='promotion-filter'),
    path('all/', views.PromotionListAPIView.as_view(), name='promotion'),
    path('create/', views.PromotionCreateAPIView.as_view(), name='promotion-create'),
    path('<int:pk>/', views.PromotionDetailAPIView.as_view(), name='promotion-detail'),
    path('like/<int:pk>/', views.LikeCounterView.as_view(), name='promotion-likes'),
    path('favorite/<int:pk>/', views.FavoriteCounterView.as_view(), name='promotion-favorites'),
    path('my/', views.MyPromotionList.as_view(), name='promotion-my'),
    path('my/del/<int:pk>/', views.MyPromotionDelete.as_view(), name='promotion-my-del'),
    path('likes/', views.UserLikePromotionsAPIView.as_view(), name='like-promotions'),
    path('favorites/', views.UserFavoritePromotionsAPIView.as_view(), name='favorite-promotions'),
    path('hint/', views.PromotionHintListAPIVIew.as_view(), name='promotion-hint'),
]
