from django.urls import path

from user.api import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('me/<int:pk>', views.CustomUserViewSet.as_view(
        {'get': 'retrieve',
         'put': 'update',
         'delete': 'destroy'}), name='user-me'),
]
