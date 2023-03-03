from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(verbose_name='Имя жанра', max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения', max_length=256
    )
    year = models.IntegerField(verbose_name='Год выхода', )
    description = models.TextField(verbose_name='Краткое описание', )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre}'


class Publication(models.Model):
    text = models.TextField(
        verbose_name="Публикация",
        help_text="Текст публикации"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Дата публикации"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name="Автор",
        help_text="Автор публикации"
    )

    class Meta:
        abstract = True
        ordering = ['id']


class Review(Publication):
    score = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name="Оценка",
        help_text="Оцените произведение от 1 до 10"
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return self.text

    class Meta(Publication.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(Publication):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name="Комментируемое произведение",
        help_text="Оставьте свой комментарий"
    )

    def __str__(self):
        return self.text

    class Meta(Publication.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
