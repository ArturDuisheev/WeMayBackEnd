from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.api import views

urlpatterns = [
    # Auth
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),

    # OAuth
    path('oauth/facebook/', views.FacebookOAuthAPIView.as_view(), name='oauth_facebook'),
    path('oauth/google/', views.GoogleOAuthAPIView.as_view(), name='oauth_google'),

    # Profile (Change user's credentials)
    path('profile/', views.UserProfileAPIView.as_view(), name='profile'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
