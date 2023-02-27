from rest_framework import serializers

from .models import ReviewUser


class ReviewUserSerializer(serializers.ModelSerializer):
    """Получение данных пользователя"""
    class Meta:
        model = ReviewUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role')


class CreateUserSerializer(serializers.ModelSerializer):
    """Создание нового пользователя"""
    class Meta:
        model = ReviewUser
        fields = ('username', 'email')


class CreateTokenSerializer(serializers.ModelSerializer):
    """Создание токена"""
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)