from .base_validator import Validator
from ..exceptions import ValueExists
from db.models import Number


class NumberValidator(Validator):
    example = '9123456789'
    regex = r'^[\d]{10}$'

    @classmethod
    def post_validate(cls, value, bot, pm):
        if Number.manager().has(number=value):
            raise ValueExists(bot, pm, value)
        return True
