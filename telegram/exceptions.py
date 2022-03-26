from .messages import ErrorMessages


class TelegramBotException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class AccessForbidden(TelegramBotException):
    def __init__(self) -> None:
        super().__init__(ErrorMessages.FORBIDDEN)
