from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet


router = SimpleRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)

urlpatterns = [
    path('v1/', include(router.urls))
]
