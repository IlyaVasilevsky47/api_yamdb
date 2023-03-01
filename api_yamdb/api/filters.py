from django_filters import rest_framework
from reviews.models import Category, Genre, Review, Title

class AriticleFilter(rest_framework.FilterSet):
    min_read = rest_framework(field_name='read_num', lookup_expr='gte')
    max_read = rest_framework.NumberFilter(field_name='read_num', lookup_expr='lte')
    title = rest_framework.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ['title', 'category', 'min_read', 'max_read']