from datetime import date, timedelta

from django.db.models import Count

from rest_framework.response import Response
from rest_framework import generics, status, views, filters, permissions

from django_filters.rest_framework import DjangoFilterBackend
from company.models import Contact

from promotion.models import PromotionCategory, Promotion, PromotionAddress
from promotion.paginations import CustomPagePagination
from .serializers import ContactSerializer, PromotionCategorySerializer, PromotionSerializer, MyPromotionSerializer, FavoritePromotionSerializer


class PromotionCategoryCreateAPIView(generics.CreateAPIView):
    serializer_class = PromotionCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class PromotionCategoryListAPIView(generics.ListAPIView):
    queryset = PromotionCategory.objects.all()
    serializer_class = PromotionCategorySerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class PromotionCategoryDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = PromotionCategory.objects.all()
    serializer_class = PromotionCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PromotionListAPIView(generics.ListAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['title', 'description', 'type', 'address',
                        'category__title', 'type', 'discount', 'likes',
                        'company__name']

    def get_queryset(self):
        queryset = Promotion.objects.annotate(Count('likes')).order_by('-likes__count')
        filter = self.kwargs.get('filter')

        filter_dict = {
            'free': queryset.filter(new_price=0),
            'daily': queryset.filter(is_daily=True),
            'liked': queryset.filter(likes__email=self.request.user),
            'end_soon': queryset.filter(
                end_date__lte=date.today() + timedelta(days=3),
                end_date__gte=date.today()
            ),
        }

        return filter_dict.get(filter) if filter in filter_dict else queryset


class PromotionCreateAPIView(generics.CreateAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.AllowAny]


class PromotionDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


from promotion.api.serializers import LikeCounterSerializer
from rest_framework.parsers import JSONParser

class LikeCounterView(generics.CreateAPIView):
    serializer_class = LikeCounterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        promotion_id = kwargs.get('pk')
        
        promotion = Promotion.objects.filter(pk=promotion_id).first()

        if not promotion:
            return Response(
                {'message': 'Акция не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        like_count = promotion.likes.count()

        return Response(
            {'likes_count': like_count},
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        promotion_id = kwargs.get('pk')
        
        promotion = Promotion.objects.filter(pk=promotion_id).first()

        if not promotion:
            return Response(
                {'message': 'Акция не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user in promotion.likes.all():
            promotion.likes.remove(request.user)
            return Response(
                {'message': 'Лайк удален'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {'message': 'Лайк не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, *args, **kwargs):
        promotion_id = kwargs.get('pk')
        
        promotion = Promotion.objects.filter(pk=promotion_id).first()

        if not promotion:
            return Response(
                {'message': 'Акция не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        if user not in promotion.likes.all():
            promotion.likes.add(user)
            like_count = promotion.likes.count()

            return Response(
                {'message': 'Добавлено в \'Понравившиеся акции\'',
                 'count': like_count},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': 'Вы уже поставили лайк на эту акцию'},
                status=status.HTTP_400_BAD_REQUEST
            )


from promotion.api import permissons as pr_per

class ContactView(generics.CreateAPIView):

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class MyPromotionList(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = MyPromotionSerializer
    permission_classes = [pr_per.IsOwnerOrReadOnly]


class MyPromotionDelete(generics.DestroyAPIView):
    queryset = Promotion.objects.all()
    serializer_class = MyPromotionSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'



class UserFavoritePromotionsAPIView(generics.ListAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [pr_per.IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Promotion.objects.filter(likes=user)

from promotion.api.serializers import AddressSerializer

class AddressCreateAPIView(generics.CreateAPIView):
    queryset = PromotionAddress.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

