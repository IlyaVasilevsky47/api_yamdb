from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet


router = SimpleRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]
