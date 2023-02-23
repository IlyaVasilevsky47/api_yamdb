from rest_framework import viewsets

from reviews.models import Category, Genre, Title, Review, Comment

from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer
)


# Запросы GET, POST, DEL
# Фильтр:
# search, string - Поиск по названию категории
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Запросы GET, POST
# Фильтр:
# search, string - Поиск по названию жанра
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


# Запросы GET, POST, id_title запросы к GET, POST, PATCH, DEL
# Фильтр:
# 1. category, string - фильтрует по полю slug категории
# 2. genre, string - фильтрует по полю slug жанра
# 3. name, string - фильтрует по названию произведения
# 4. year, integer - фильтрует по году
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


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
        review_id = self.kwargs.get("review_id")
        queryset = Comment.objects.filter(review=review_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get("review_id")
        )
