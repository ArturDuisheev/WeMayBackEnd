from django.urls import path
from .api import views

urlpatterns = [
    path('all/', views.CompanyListAPIView.as_view()),
    path('all/<str:my>/', views.CompanyListAPIView.as_view()),
    path('create/', views.CompanyCreateAPIView.as_view()),
    path('<int:pk>/', views.CompanyDetailAPIView.as_view()),

    path('<int:pk>/contact/all/', views.ContactListAPIView.as_view()),
    path('<int:pk>/contact/create/', views.ContactCreateAPIView.as_view()),
    path('contact/<int:pk>/', views.ContactDetailAPIView.as_view()),
]
