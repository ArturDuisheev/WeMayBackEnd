from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import generics, status, permissions, views, filters

from promotion.paginations import CustomLimitOffsetPagination
from review.models import Review
from .serializers import ReviewSerializer
from review.utils.limit_rate import limit_rate as ratelimit
from review import services as rev_ser


class ReviewListAPIVIew(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['created_time']
    pagination_class = CustomLimitOffsetPagination
    lookup_url_kwarg = 'promotion'

    def get_queryset(self):
        promotion_pk = self.kwargs.get(self.lookup_url_kwarg)
        queryset = super().get_queryset().filter(promotion_id=promotion_pk)
        return queryset


class ReviewCreateAPIVIew(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    @ratelimit(num_requests=3, period=3600)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            author = request.user
            serializer.validated_data['author'] = author
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def patch(self, request, *args, **kwargs):
        review = self.get_object()

        if review.author == self.request.user:
            return super().patch(request, *args, **kwargs)

        return Response(
            {'message': 'У вас нет разрешения на изменение этого отзыва'},
            status=status.HTTP_403_FORBIDDEN
        )

    def put(self, request, *args, **kwargs):
        return Response(
            {'message': 'Method PUT not allowed'},
            status=status.HTTP_403_FORBIDDEN
        )

    def delete(self, request, *args, **kwargs):
        review = self.get_object()

        if review.author == self.request.user:
            review.delete()
            return Response(
                {'message': 'Отзыв успешно удален'},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {'message': 'У вас нет разрешения на удаление этого отзыва'},
            status=status.HTTP_403_FORBIDDEN
        )


class LikeCounterView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        review_id = kwargs.get('pk')
        like_count = rev_ser.get_like_count(review_id)
        if like_count is None:
            return Response({'message': 'отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'likes_count': like_count}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        review_id = kwargs.get('pk')
        success, message = rev_ser.toggle_like_status(review_id, request.user)
        if not success:
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': message}, status=status.HTTP_201_CREATED)