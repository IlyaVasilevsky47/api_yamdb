from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework import filters, permissions, serializers
from rest_framework.permissions import IsAdminUser
from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import ReviewUser
from .permissions import Admin_ReadOnly_Permission, All_Permission, Admin_Auth_Permission
from .serializers import ReviewUserSerializer, CreateUserSerializer, CreateTokenSerializer


from api.permissions import IsAuthorOrReadOnly
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
        queryset = get_object_or_404(Title, id=title_id).reviews.all()
        return queryset

    def perform_create(self, serializer):
        try:
            serializer.save(
                author=self.request.user,
                title_id=self.kwargs.get("title_id")
            )
        except Exception:
            raise serializers.ValidationError('Вы уже оставляли отзыв')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminUser]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        queryset = get_object_or_404(Review, id=review_id).comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get("review_id")
        )


class ReviewUserViewSet(viewsets.ModelViewSet):
    queryset = ReviewUser.objects.all()
    serializer_class = ReviewUserSerializer
    permission_classes = (Admin_Auth_Permission,)
    # pagination_class = 1

    @action(
        methods=('patch', 'get'),
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
        url_name='me'
    )
    def me_edit_profile(self,request, *args, **kwargs):
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

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_new_user(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    serializer.save()
    confirmation_code = default_token_generator.make_token(
        ReviewUser.objects.get(email=email, username=username)
    )
    token_message = f'Код подтверждения для {username}: {confirmation_code}'
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
    user = get_object_or_404(ReviewUser, username=username)
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