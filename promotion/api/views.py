from django.db.models import Count
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from promotion.models import PromotionCategory, Promotion
from .serializers import PromotionCategorySerializer, PromotionSerializer
# Create your views here.


class PromotionCategoryListAPIView(generics.ListCreateAPIView):
    queryset = PromotionCategory.objects.all()
    serializer_class = PromotionCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class PromotionCategoryDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = PromotionCategory.objects.all()
    serializer_class = PromotionCategorySerializer
    permission_classes = [IsAuthenticated]


class PromotionListAPIView(generics.ListCreateAPIView):
    # Annotate queryset to sort the promotions by the quantity of their likes
    queryset = Promotion.objects.annotate(Count('likes')).order_by('-likes__count')
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'type', 'address']
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'type', 'discount', 'likes']


class PromotionDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]


class LikeCounterView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, pk):
        promotion = Promotion.objects.filter(category_id=id, pk=pk).first()

        if not promotion:
            return Response({'detail': 'Акция не найдена'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the count of likes for the specified promotion
        Like = promotion.likes.through
        like_count = Like.objects.count()

        return Response({'count': like_count}, status=status.HTTP_200_OK)

    def post(self, request, id, pk):
        user = self.request.user
        promotion = Promotion.objects.filter(category_id=id, pk=pk).first()

        if not promotion:
            return Response({'detail': 'Акция не найдена'}, status=status.HTTP_404_NOT_FOUND)

        Like = promotion.likes.through
        current_like = Like.objects.filter(myuser_id=user.id)

        # Check if current user has already liked the promotion
        if current_like.exists():
            return Response({'message': 'Вы уже поставили лайк на эту акцию'},
                            status=status.HTTP_400_BAD_REQUEST)

        current_like.create(promotion_id=promotion.id, myuser_id=user.id)
        like_count = current_like.count()

        return Response({'message': 'Добавлено в \'Понравившиися акции\'', 'count': like_count})

    def delete(self, request, id, pk):
        # Check if the user has already liked the promotion
        user = self.request.user
        promotion = Promotion.objects.filter(category_id=id, pk=pk).first()

        if not promotion:
            return Response({'detail': 'Акция не найдена'}, status=status.HTTP_404_NOT_FOUND)

        # Get the intermediate table and get the current user's like
        Like = promotion.likes.through
        current_like = Like.objects.filter(myuser_id=user.id)

        if not current_like:
            return Response({'message': 'Вы уже удалили лайк'})
        current_like.delete()
        return Response({'message': 'Лайк удален'})
