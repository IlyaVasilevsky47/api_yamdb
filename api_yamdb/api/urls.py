from rest_framework.routers import SimpleRouter
from rest_framework import routers
from django.conf.urls import url, include

from django.urls import include, path


from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet, ReviewUserViewSet, create_new_user, create_jwt_token
)


router = SimpleRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
router.register(r'users', ReviewUserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', create_new_user),
    path('v1/auth/token/', create_jwt_token),
]
