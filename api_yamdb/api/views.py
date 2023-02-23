from rest_framework import viewsets, mixins
from rest_framework import filters

from reviews.models import Category, Genre, Title

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


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
