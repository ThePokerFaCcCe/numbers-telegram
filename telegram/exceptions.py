from .messages import ErrorMessages


class TelegramBotException(Exception):
    _default_message = None

    def __init__(self, pm, message=None, **format_kwargs) -> None:
        self.pm = pm
        message = message or self._default_message
        self.message = message.format(**format_kwargs)


class AccessForbidden(TelegramBotException):
    _default_message = ErrorMessages.FORBIDDEN


class InvalidInput(TelegramBotException):
    _default_message = ErrorMessages.INVALID

    def __init__(self, pm, example=None):
        super().__init__(pm, example=example)


class ValueExists(TelegramBotException):
    _default_message = ErrorMessages.EXISTS

    def __init__(self, pm, value=None):
        super().__init__(pm, value=value)
