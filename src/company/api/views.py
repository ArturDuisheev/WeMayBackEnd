from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response

from promotion.paginations import CustomPagePagination
from .serializers import CompanySerializer, ContactSerializer
from company.models import Company, Contact


class ContactCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.all()


class ContactListAPIView(generics.ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Contact.objects.filter(company_id=self.kwargs.get('pk'))


class ContactDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CompanyCreateAPIView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        data['owner'] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'message': 'Вы успешно создали компанию'},
            status=status.HTTP_201_CREATED
        )


class CompanyListAPIView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'discounts', 'description', 'owner']
    pagination_class = CustomPagePagination

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user) if self.kwargs.get('my') else Company.objects.all()


class CompanyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        company = self.get_object()

        if company.owner == self.request.user:
            return super().patch(request, *args, **kwargs)

        return Response(
            {'message': 'У вас нет разрешения на изменение этой компании'},
            status=status.HTTP_403_FORBIDDEN
        )

    def put(self, request, *args, **kwargs):
        return Response(
            {'message': 'Method PUT not allowed'},
            status=status.HTTP_403_FORBIDDEN
        )

    def delete(self, request, *args, **kwargs):
        company = self.get_object()

        if company.owner == self.request.user:
            company.delete()
            return Response(
                {'message': 'Компания успешно удалена'},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {'message': 'У вас нет разрешения на удаление этой компании'},
            status=status.HTTP_403_FORBIDDEN
        )
