from django.urls import path

from user.api.views import RegisterAPIView, LogInView, LogoutView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
