from rest_framework.response import Response
from rest_framework import generics, status, permissions, views

from review.models import Review
from .serializers import ReviewSerializer


class ReviewListCreateAPIVIew(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


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
