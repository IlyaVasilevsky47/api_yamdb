import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username_not_me(value):
    """Проверка, чтоб 'username' не было присвоено 'me' """
    if value.lower() == 'me':
        raise ValidationError(
            'Выберите другое обозначение для username'
        )
    if not re.match('^[\w.@+-]+\z', value):
        raise ValidationError(
            'Выбранные символы не подходят для username'
        )