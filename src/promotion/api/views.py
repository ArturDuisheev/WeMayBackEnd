from datetime import date, timedelta

from django.db.models import Count

from rest_framework.response import Response
from rest_framework import generics, status, views, filters, permissions

from django_filters.rest_framework import DjangoFilterBackend
from company.models import Contact

from promotion.models import PromotionCategory, Promotion
from promotion.paginations import CustomPagePagination
from .serializers import ContactSerializer, PromotionCategorySerializer, PromotionSerializer


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
    permission_classes = [permissions.IsAuthenticated]


class LikeCounterView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        promotion = Promotion.objects.filter(pk=pk).first()

        if not promotion:
            return Response(
                {'message': 'Акция не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Retrieve the count of likes for the specified promotion
        Like = promotion.likes.through
        like_count = Like.objects.count()

        return Response(
            {'likes_count': like_count},
            status=status.HTTP_200_OK
        )

    def post(self, request, pk):
        user = self.request.user
        promotion = Promotion.objects.filter(pk=pk).first()

        if not promotion:
            return Response(
                {'message': 'Акция не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        Like = promotion.likes.through
        current_like = Like.objects.filter(myuser_id=user.id)

        # Check if current user has already liked the promotion
        if current_like.exists():
            return Response(
                {'message': 'Вы уже поставили лайк на эту акцию'},
                status=status.HTTP_400_BAD_REQUEST
            )

        current_like.create(promotion_id=promotion.id, myuser_id=user.id)
        like_count = current_like.count()

        return Response(
            {'message': 'Добавлено в \'Понравившиеся акции\'',
             'count': like_count},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        # Check if the user has already liked the promotion
        user = self.request.user
        promotion = Promotion.objects.filter(pk=pk).first()

        if not promotion:
            return Response(
                {'message': 'Акция не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get the intermediate table and get the current user's like
        Like = promotion.likes.through
        current_like = Like.objects.filter(myuser_id=user.id)

        if not current_like:
            return Response(
                {'message': 'Вы уже удалили лайк'},
                status=status.HTTP_204_NO_CONTENT
            )
        current_like.delete()

        return Response(
            {'message': 'Лайк удален'},
            status=status.HTTP_204_NO_CONTENT
        )



class ContactView(generics.CreateAPIView):

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer