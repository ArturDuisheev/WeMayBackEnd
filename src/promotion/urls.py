from django.urls import path
from .api import views

urlpatterns = [
    path('category/create/', views.PromotionCategoryCreateAPIView.as_view(), name='category-create'),
    path('category/all/', views.PromotionCategoryListAPIView.as_view(), name='category'),
    path('category/<int:pk>/', views.PromotionCategoryDetailAPIView.as_view(), name='category-detail'),

    # Path filter (free, end_soon, daily, liked) are used to filter the objects by these fields
    path('all/<str:filter>/', views.PromotionListAPIView.as_view(), name='promotion-filter'),
    path('all/', views.PromotionListAPIView.as_view(), name='promotion'),
    path('create/', views.PromotionCreateAPIView.as_view(), name='promotion-create'),
    path('<int:pk>/', views.PromotionDetailAPIView.as_view(), name='promotion-detail'),
    path('<int:pk>/like/', views.LikeCounterView.as_view(), name='promotion-likes'),
    path('my/', views.MyPromotionList.as_view(), name='promotion-my'),
    path('my/del/<int:pk>/', views.MyPromotionDelete.as_view(), name='promotion-my-del'),
    path('favorite/', views.UserFavoritePromotionsAPIView.as_view(), name='favorite-promotion'),
    path('address-create/', views.AddressCreateAPIView.as_view(), name='address-create'),
]

