from rest_framework.response import Response
from rest_framework import generics, status, permissions, views

from review.models import Review
from .serializers import ReviewSerializer


class ReviewListCreateAPIVIew(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        user = self.request.user

        if not user.username or user.username == '':
            return Response({'message': 'Вы не можете оставлять отзывы без \'username\'.'
                                        ' Пожалуйста заполните это поле'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['author'] = user.id
        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            return Response({'message': 'Неправильный формат данных'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'message': 'Отзыв успешно создан'},
                        status=status.HTTP_201_CREATED)


class MyReviewListAPIVIew(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(author=user)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        review = self.get_object()
        if review.author == self.request.user:
            return super().put(request, *args, **kwargs)

        return Response(
            {"Сообщение": "У вас нет разрешения на изменение этого отзыва"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def patch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.author == self.request.user:
            return super().patch(request, *args, **kwargs)

        return Response(
            {"Сообщение": "У вас нет разрешения на изменение этого отзыва"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if review.author == self.request.user:
            review.delete()
            return Response(
                {"Сообщение": "Отзыв успешно удален"}, status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {"Сообщение": "У вас нет разрешения на удаление этого отзыва"},
            status=status.HTTP_403_FORBIDDEN
        )


class LikeCounterView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        review = Review.objects.filter(pk=pk).first()

        if not review:
            return Response({'detail': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the count of likes for the specified review
        Like = review.likes.through
        like_count = Like.objects.count()

        return Response({'count': like_count}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        user = self.request.user
        review = Review.objects.filter(pk=pk).first()

        if not review:
            return Response({'detail': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)

        Like = review.likes.through
        current_like = Like.objects.filter(myuser_id=user.id)

        # Check if current user has already liked the review
        if current_like.exists():
            return Response({'message': 'Вы уже поставил лайк на этот отзыв'},
                            status=status.HTTP_400_BAD_REQUEST)

        current_like.create(review_id=review.id, myuser_id=user.id)
        like_count = current_like.count()

        return Response({'message': 'Добавлено в \'Понравившиися акции\'', 'count': like_count})

    def delete(self, request, pk):
        # Check if the user has already liked the review
        user = self.request.user
        review = Review.objects.filter(pk=pk).first()

        if not review:
            return Response({'detail': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Get the intermediate table and get the current user's like
        Like = review.likes.through
        current_like = Like.objects.filter(myuser_id=user.id)

        if not current_like:
            return Response({'message': 'Вы уже удалили лайк'})
        current_like.delete()
        return Response({'message': 'Лайк удален'})
