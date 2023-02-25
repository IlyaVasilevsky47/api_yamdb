from django.conf.urls import url, include
from django.urls import include, path
from rest_framework import routers

from .views import ReviewUserViewSet, create_new_user, create_jwt_token


router_v1 = routers.DefaultRouter()
router_v1.register('users', ReviewUserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', create_new_user),
    path('v1/auth/token/', create_jwt_token),
    url(r'^verified-email-field/', include('verified_email_field.urls')),
]