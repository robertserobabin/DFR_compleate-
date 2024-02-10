import re
from rest_framework.serializers import ValidationError


class LinkValidator:
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        reg = re.compile('https://youtube.com')
        tmp = dict(value).get(self.fields)
        if not bool(reg.match(tmp)):
            raise ValidationError('ошибка')

