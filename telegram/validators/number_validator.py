from .base_validator import Validator
from ..exceptions import ValueExists, ValueNotExists
from db.models import Number


class BaseNumberValidator(Validator):
    example = '9123456789'
    regex = r'^[\d]{10}$'


class AddNumberValidator(BaseNumberValidator):
    @classmethod
    def post_validate(cls, pm):
        value = str(int(pm.text))
        if Number.manager().has(number=value):
            raise ValueExists(pm, value)
        return value


class DeleteNumberValidator(BaseNumberValidator):
    @classmethod
    def post_validate(cls, pm):
        value = str(int(pm.text))
        if not Number.manager().has(number=value):
            raise ValueNotExists(pm, value)
        return value
