from typing import Callable
from decouple import config
from telebot import TeleBot
from telebot.types import Message

from db.models import Admin
from .messages import InfoMessages
from . import exceptions

ACCESS_PASSWORD = config("ACCESS_PASSWORD")


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
        bot = TeleBot(config("BOT_TOKEN"), threaded=False)
        self.__bot = bot

        @bot.message_handler(commands=['access'])
        def handle_access(pm): self.handle_access(pm)

        @bot.message_handler(commands=['start'])
        def handle_start(pm): self.call_admin_handler(self.handle_start, pm)

    def call_admin_handler(self, handler: Callable, pm: Message):
        try:
            if not pm.chat.id in self.admins:
                raise exceptions.AccessForbidden()
            handler(pm)
        except exceptions.TelegramBotException as e:
            self.bot.reply_to(pm, e.message)

    def handle_start(self, pm: Message):
        """Send welcome message"""
        self.bot.reply_to(pm, InfoMessages.WELCOME)

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
            return self.bot.reply_to(pm, InfoMessages.ACCESS_ALREADY)

        Admin(user_id=chatid).save(commit=True)
        self.update_admins()
        self.bot.reply_to(pm, InfoMessages.ACCESS_SUCCESS)

    def run(self):
        self.bot.polling()
