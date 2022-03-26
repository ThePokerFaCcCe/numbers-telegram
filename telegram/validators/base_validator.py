import re
from ..exceptions import InvalidInput


class Validator:
    example = None
    regex = None

    @classmethod
    def validate(cls, pm):
        """Raise `InvalidInput` if `pm.text` wasn't valid"""
        if not bool(re.match(cls.regex, pm.text)):
            raise InvalidInput(pm, cls.example)
        return cls.post_validate(pm)

    @classmethod
    def post_validate(cls, pm):
        """This method will be called after `validate()`"""
        return True
