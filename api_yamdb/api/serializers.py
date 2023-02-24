from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=256, source='name')
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(),
                message='Такой slug уже есть в базе данных',
            )
        ]
    )

    class Meta:
        fields = ('category_name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(max_length=256, source='name')
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Genre.objects.all(),
                message='Такой slug уже есть в базе данных',
            )
        ]
    )

    class Meta:
        fields = ('genre_name', 'slug')
        model = Genre


# Сделать валидацию года
class TitleSerializer(serializers.ModelSerializer):
    # genre = GenreSerializer(required=False, many=True)
    # category = CategorySerializer(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
        read_only_fields = ('')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        model = Comment
