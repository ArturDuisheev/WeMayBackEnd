from django.urls import path
from .api import views

urlpatterns = [
    path('category/all/', views.PromotionCategoryListCreateAPIView.as_view(), name='category'),
    path('category/<int:pk>/', views.PromotionCategoryDetailAPIView.as_view(), name='category-detail'),
    path('all/', views.PromotionListAPIView.as_view()),

    # Path filter (free, end_soon, daily, liked) are used to filter the objects by these fields
    path('all/<str:path_filter>/', views.PromotionListAPIView.as_view()),
    path('create/', views.PromotionCreateAPIView.as_view()),
    path('<int:pk>/', views.PromotionDetailAPIView.as_view()),
    path('<int:pk>/like/', views.LikeCounterView.as_view()),
    path('<int:pk>', views.PromotionListAPIView.as_view()),
]
