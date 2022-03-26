import re
from ..exceptions import InvalidInput


class Validator:
    example = None
    regex = None

    @classmethod
    def validate(cls, value, bot, pm):
        """Raise `InvalidInput` if value wasn't valid"""
        if not bool(re.match(cls.regex, value)):
            raise InvalidInput(bot, pm, cls.example)
        return cls.post_validate(value, bot, pm)

    @classmethod
    def post_validate(cls, value, bot, pm):
        """This method will be called after `validate()`"""
        return True
