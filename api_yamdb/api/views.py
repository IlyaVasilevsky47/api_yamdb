from rest_framework import viewsets, mixins
from rest_framework import filters, permissions
from rest_framework.permissions import IsAdminUser

from api.permissions import IsAuthorOrReadOnly
# from users.permissions import Admin_ReadOnly_Permission
from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    CategorySerializer, GenreSerializer, GetTitleSerializer,
    PostPatchTitleSerializer, ReviewSerializer, CommentSerializer
)


class ListCreateDestroy(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (Admin_ReadOnly_Permission,)
    filter_bckends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (Admin_ReadOnly_Permission,)
    filter_bckends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # permission_classes = ('Admin_ReadOnly_Permission',)
    filter_bckends = (filters.SearchFilter, )
    search_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return GetTitleSerializer
        return PostPatchTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminUser]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        queryset = Review.objects.filter(title=title_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get("title_id")
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminUser]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        queryset = Comment.objects.filter(review=review_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get("review_id")
        )
