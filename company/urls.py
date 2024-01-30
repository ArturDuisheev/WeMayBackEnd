from django.urls import path
from api.views import CompanyListCreateAPIView, CompanyDetailAPIView

urlpatterns = [
    path('company/all/', CompanyListCreateAPIView.as_view()),
    path('company/<int:pk>/', CompanyDetailAPIView.as_view()),
]
