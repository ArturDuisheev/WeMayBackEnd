from rest_framework import generics
from company.models import Company
from .serializers import CompanySerializer


class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


