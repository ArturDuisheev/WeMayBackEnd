from django.urls import path
from company.api.views import CompanyListCreateAPIView

urlpatterns = [
    path('company/', CompanyListCreateAPIView.as_view())
]