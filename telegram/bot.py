from typing import Callable
from decouple import config
from telebot import TeleBot, types, ExceptionHandler
from telebot.types import Message

from db.models import Admin, Number
from .messages import InfoMessages, ButtonTexts
from .validators import NumberValidator
from . import exceptions

ACCESS_PASSWORD = config("ACCESS_PASSWORD")


class BotExceptionHandler(ExceptionHandler):
    def handle(self, e):
        if isinstance(e, exceptions.TelegramBotException):
            e.bot.reply_to(e.pm, e.message)
            return True


class NumberBot:
    __admins: list
    __bot: TeleBot

    @property
    def bot(self):
        return self.__bot

    @property
    def admins(self):
        return self.__admins

    def update_admins(self):
        """Update admins array"""
        self.__admins = [admin.user_id for admin in
                         Admin.manager().all()]

    def __init__(self) -> None:
        self.update_admins()
        bot = TeleBot(config("BOT_TOKEN"), threaded=False,
                      exception_handler=BotExceptionHandler())
        self.__bot = bot

        @bot.message_handler(commands=['access'])
        def handle_access(pm): self.handle_access(pm)

        @bot.message_handler(commands=['start'])
        def handle_start(pm): self.call_admin_handler(self.handle_start, pm)

        @bot.message_handler(func=lambda pm: pm.text == ButtonTexts.ADD_NUMBER)
        def handle_start(pm): self.call_admin_handler(self.handle_add_number, pm)

    def call_admin_handler(self, handler: Callable, pm: Message):
        if not pm.chat.id in self.admins:
            raise exceptions.AccessForbidden(self.bot, pm)
        handler(pm)

    def handle_start(self, pm: Message):
        """Send welcome message"""
        self.bot.reply_to(pm, InfoMessages.WELCOME, reply_markup=self.markup)

    def handle_access(self, pm: Message):
        """Add user to admins if it wasn't admin already"""
        text = pm.text.split(' ', 1)
        if len(text) < 2:
            return

        password = text[-1]
        if password != ACCESS_PASSWORD:
            return

        chatid = pm.chat.id

        if chatid in self.admins:
            return self.bot.reply_to(pm, InfoMessages.ACCESS_ALREADY,
                                     reply_markup=self.markup)

        Admin(user_id=chatid).save()
        self.update_admins()
        self.bot.reply_to(pm, InfoMessages.ACCESS_SUCCESS,
                          reply_markup=self.markup)

    def handle_add_number(self, pm: Message):
        """Add number to database"""
        msg = self.bot.reply_to(
            pm,
            InfoMessages.INPUT_NUMBER.format(example=NumberValidator.example)
        )
        self.bot.register_next_step_handler(msg, self.next_handler_add_number)

    def next_handler_add_number(self, pm: Message):
        number_text = pm.text
        NumberValidator.validate(number_text, self.bot, pm)

        number = Number(number=number_text).save()
        self.bot.reply_to(
            pm,
            InfoMessages.ADD_NUMBER_SUCCESS.format(number=number.number),
            reply_markup=self.markup
        )

    def run(self):
        self.bot.infinity_polling()

    @property
    def markup(self):
        """Return keyboard markup"""
        mk = types.ReplyKeyboardMarkup(True, True, row_width=1)
        mk.add(ButtonTexts.ADD_NUMBER)
        mk.add(ButtonTexts.EXPORT)
        return mk
