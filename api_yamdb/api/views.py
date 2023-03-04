from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import ReviewUser

from .filters import TitleFilter
from .permissions import (IsAdminAuth, IsAdminOrReadOnly,
                          IsReadOnlyAuthorAdminModeratorAuth)
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateTokenSerializer, CreateUserSerializer,
                          GenreSerializer, GetTitleSerializer,
                          PostPatchTitleSerializer, ReviewSerializer,
                          ReviewUserSerializer)

User = get_user_model()


class ListCreateDestroy(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg('reviews__score')).order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    search_fields = ['category', 'genre', 'name', 'year']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return GetTitleSerializer
        return PostPatchTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReadOnlyAuthorAdminModeratorAuth]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        queryset = get_object_or_404(Title, id=title_id).reviews.all()
        return queryset

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsReadOnlyAuthorAdminModeratorAuth]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        queryset = get_object_or_404(Review, id=review_id).comments.all()
        return queryset

    def get_review(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review())


class ReviewUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ReviewUserSerializer
    permission_classes = (IsAdminAuth,)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=('patch', 'get'),
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
        url_name='me'
    )
    def me_edit_profile(self, request, *args, **kwargs):
        isinstance = self.request.user
        serializer = self.get_serializer(isinstance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                isinstance,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=self.request.user.role)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if self.request.method == 'PUT':
            return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_new_user(request):
    serializer = CreateUserSerializer(data=request.data)

    email = request.data.get('email')
    username = request.data.get('username')
    is_present = ReviewUser.objects.filter(
        email=email, username=username
    ).exists()

    if is_present:
        serializer.is_valid()
    else:
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        serializer.save()

    confirmation_code = default_token_generator.make_token(
        User.objects.get(email=email, username=username)
    )
    token_message = (f'Код подтверждения для {username}:'
                     f'{confirmation_code}')
    send_mail(
        message=token_message,
        subject='Confirmation code',
        recipient_list=[email],
        from_email=None
    )
    return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_jwt_token(request):
    serializer = CreateTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            data={'token': str(token)},
            status=HTTPStatus.OK
        )
    return Response(
        'Код подтверждения или пользователь указан неверно',
        status=HTTPStatus.BAD_REQUEST
    )
