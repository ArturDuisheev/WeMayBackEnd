from django.urls import path

from user.api import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register')
]
