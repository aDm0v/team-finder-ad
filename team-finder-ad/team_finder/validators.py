import re

from django.core.exceptions import ValidationError


def validate_github_url(value):
    if value and not re.match(r'^https://github\.com/', value):
        raise ValidationError(
            'Укажите корректный URL GitHub (должен начинаться с https://github.com/)'
        )


def validate_phone(value):
    if value and not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', value):
        raise ValidationError('Введите корректный номер телефона')
