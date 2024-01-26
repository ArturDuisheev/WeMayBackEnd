from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from promotion.models import PromotionCategory, Promotion, Like
from .serializers import PromotionCategorySerializer, PromotionSerializer, LikeSerializer
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
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'type', 'address']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'type', 'discount']


class PromotionDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]


class LikeCounterView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, pk, like_pk):
        # Retrieve the count of likes for the specified promotion
        promotion = Promotion.objects.filter(pk=like_pk).first()

        if promotion:
            like_count = Like.objects.filter(promotion=promotion).count()
            data = {'count': like_count}
            serializer = LikeSerializer(data=data)
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Promotion not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, promotion_id):
        # Check if the user has already liked the promotion
        user = self.request.user
        if Like.objects.filter(user=user, promotion_id=promotion_id).exists():
            return Response({'message': 'already liked'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create a new like
        like_data = {'user': user.id, 'promotion': promotion_id}
        serializer = LikeSerializer(data=like_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, promotion_id):
        # Check if the user has already liked the promotion
        user = self.request.user
        try:
            like = Like.objects.get(user=user, promotion_id=promotion_id)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
