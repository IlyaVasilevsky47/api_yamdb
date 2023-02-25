from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import ReviewUser
from .permissions import Admin_ReadOnly_Permission, All_Permission, Admin_Auth_Permission
from .serializers import ReviewUserSerializer, CreateUserSerializer, CreateTokenSerializer


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