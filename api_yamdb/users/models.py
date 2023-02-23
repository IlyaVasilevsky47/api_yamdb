from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from verified_email_field.forms import VerifiedEmailField


class ReviewUser(AbstractUser):
    "Кастомный User с распределенными правами по ролям"
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email']
    
    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'
    SUPERUSER_ROLE = 'superuser'

    ROLE_CHOICES = (
        (USER_ROLE, 'user'),
        (MODERATOR_ROLE, 'moderator'),
        (ADMIN_ROLE, 'admin'),
        (SUPERUSER_ROLE, 'superuser'),
    )

    username = models.CharField(
        max_length=40,
        unique=True,
        verbose_name='Имя пользователя',
        help_text='Как к Вам обращаться?'
    )

    email = VerifiedEmailField(
        'e-mail',
        fieldsetup_id='user-email'
    )

    # email = models.EmailField(
    #     max_length=254,
    #     verbose_name='адрес электронной почты',
    #     help_text='Введите адрес электронной почты'
    # )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=50,
        verbose_name='Роль пользователя',
        help_text='Выберите из списка роль для пользователя'
    )

    # def email_user(self, subject, message, from_email='email', **kwargs):
    #     return super().email_user(subject, message, from_email, **kwargs)

    def __str__(self):
        return self.username
