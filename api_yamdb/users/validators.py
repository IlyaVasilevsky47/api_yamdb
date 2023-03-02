import re

from django.core.exceptions import ValidationError


def validate_username_not_me(value):
    """Проверка, чтоб 'username' не было присвоено 'me' """
    if value.lower() == 'me':
        raise ValidationError(
            'Выберите другое обозначение для username'
        )
    if not re.match(r'[\w.@+-]+\Z', value):
        raise ValidationError(
            'Выбранные символы не подходят для username'
        )
