from rest_framework import viewsets, mixins
from rest_framework import filters

from reviews.models import Category, Genre, Title, Review, Comment

from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer
)


class ListCreateDestroy(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = ('',)
    filter_bckends = (filters.SearchFilter, )
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = ('',)
    filter_bckends = (filters.SearchFilter, )
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = ('',)
    filter_bckends = (filters.SearchFilter, )
    search_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = [AuthorOrReadOnly]

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

    def get_queryset(self):
        ...
