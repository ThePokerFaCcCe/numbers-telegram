from .messages import ErrorMessages


class TelegramBotException(Exception):
    def __init__(self, bot, pm, message: str) -> None:
        self.message = message
        self.bot = bot
        self.pm = pm


class AccessForbidden(TelegramBotException):
    def __init__(self, bot, pm):
        super().__init__(bot, pm, ErrorMessages.FORBIDDEN)


class InvalidInput(TelegramBotException):
    def __init__(self, bot, pm, example=None):
        super().__init__(
            bot, pm,
            ErrorMessages.INVALID.format(example=example)
        )


class ValueExists(TelegramBotException):
    def __init__(self, bot, pm, value=''):
        super().__init__(
            bot, pm,
            ErrorMessages.EXISTS.format(value=value)
        )
