from rest_framework.response import Response
from rest_framework import generics, status, filters, permissions
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from promotion.models import PromotionCategory, Promotion, PromotionContact
from promotion.paginations import CustomPagePagination
from .serializers import PromotionCategorySerializer, PromotionSerializer, MyPromotionSerializer, \
    PromotionContactSerializer, PromotionHintSerializer
from promotion.services import get_filtered_promotions, toggle_like_status, toggle_favorite_status, \
    get_count, get_like_count, get_favorite_count
from promotion.api import permissons as pr_per


class PromotionListAPIView(generics.ListAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['title', 'description', 'type', 'address',
                        'category__title', 'type', 'discount', 'likes',
                        'company__name']

    def get_queryset(self):
        filter = self.kwargs.get('filter')
        return get_filtered_promotions(filter)


class PromotionCreateAPIView(generics.CreateAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PromotionDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PromotionListAPIView(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['title', 'description', 'type', 'address',
                        'category__title', 'type', 'discount', 'likes',
                        'company__name']
    lookup_field = 'pk'

    def get_queryset(self):
        filter = self.kwargs.get('filter')
        return get_filtered_promotions(filter)


class FavoriteCounterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        promotion_id = kwargs.get('pk')
        favorite_count = get_favorite_count(promotion_id)
        if favorite_count is None:
            return Response({'message': 'Акция не найдена'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'favorite_count': favorite_count}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        promotion_id = kwargs.get('pk')
        success, message = toggle_favorite_status(promotion_id, request.user)
        if not success:
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': message}, status=status.HTTP_201_CREATED)


class LikeCounterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        promotion_id = kwargs.get('pk')
        like_count = get_like_count(promotion_id)
        if like_count is None:
            return Response({'message': 'Акция не найдена'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'likes_count': like_count}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        promotion_id = kwargs.get('pk')
        success, message = toggle_like_status(promotion_id, request.user)
        if not success:
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': message}, status=status.HTTP_201_CREATED)


class PromotionCategoryCreateAPIView(generics.CreateAPIView):
    serializer_class = PromotionCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class PromotionContactCreateAPIView(generics.CreateAPIView):
    queryset = PromotionContact.objects.all()
    serializer_class = PromotionContactSerializer
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


class MyPromotionList(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = MyPromotionSerializer
    permission_classes = [pr_per.IsOwnerOrReadOnly]


class MyPromotionDelete(generics.DestroyAPIView):
    queryset = Promotion.objects.all()
    serializer_class = MyPromotionSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class UserLikePromotionsAPIView(generics.ListAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [pr_per.IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Promotion.objects.filter(likes=user)


class UserFavoritePromotionsAPIView(generics.ListAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [pr_per.IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Promotion.objects.filter(favorites=user)


class PromotionHintListAPIVIew(generics.ListAPIView):
    queryset = Promotion.objects.all().order_by('likes')
    serializer_class = PromotionHintSerializer
    permission_classes = [permissions.AllowAny]
