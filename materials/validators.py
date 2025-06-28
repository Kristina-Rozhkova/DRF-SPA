from rest_framework.serializers import ValidationError


class LinkVideoValidator:
    """Проверка валидности на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com"""
    def __init__(self, field):
        self.field = field

    def __call__(self, link):
        temp_value = dict(link).get(self.field)
        if not temp_value:
            return True
        elif 'youtube.com' in temp_value:
            return True
        raise ValidationError('К материалам можно добавлять только ссылки на YouTube.')
