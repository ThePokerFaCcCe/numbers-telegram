import traceback
from typing import Callable
from decouple import config
from telebot import TeleBot, types
from telebot.types import Message

from db.models import Admin, Number
from excel import Excel
from .messages import ErrorMessages, InfoMessages, ButtonTexts
from .validators import AddNumberValidator, DeleteNumberValidator
from . import exceptions

ACCESS_PASSWORD = config("ACCESS_PASSWORD")


class NumberBot:
    __admins: list
    __bot: TeleBot

    def send_global_message(self, message):
        for admin in self.admins:
            try:
                self.bot.send_message(admin, message)
            except Exception as e:
                pass

    def handle(self, e):
        if isinstance(e, exceptions.TelegramBotException):
            self.bot.reply_to(e.pm, e.message)
        else:
            self.send_global_message(
                ErrorMessages.UNKNOWN.format(traceback=traceback.format_exc())
            )
        return True

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
        print("Connecting to bot...")
        bot = TeleBot(config("BOT_TOKEN"), threaded=False,
                      exception_handler=self)
        print("bot connected successfully")
        self.__bot = bot

        @bot.message_handler(commands=['access'])
        def handle_access(pm): self.handle_access(pm)

        @bot.message_handler(commands=['start'])
        def handle_start(pm): self.call_admin_handler(self.handle_start, pm)

        @bot.message_handler(func=lambda pm: pm.text == ButtonTexts.ADD_NUMBER)
        def handle_add_num(pm): self.call_admin_handler(
            self.handle_manage_number, pm, self.next_handler_add_number
        )

        @bot.message_handler(func=lambda pm: pm.text == ButtonTexts.DEL_NUMBER)
        def handle_del_num(pm): self.call_admin_handler(
            self.handle_manage_number, pm, self.next_handler_delete_number
        )

        @bot.message_handler(func=lambda pm: pm.text == ButtonTexts.EXPORT)
        def handle_export(pm): self.call_admin_handler(self.handle_export, pm)

    def call_admin_handler(self, handler: Callable, pm: Message, *hargs, **hkwargs):
        """Calls handler only if user is in `admins` list"""
        if not pm.chat.id in self.admins:
            raise exceptions.AccessForbidden(pm)
        handler(pm, *hargs, **hkwargs)

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

    def handle_export(self, pm: Message):
        excel = Excel()
        data = {num.number for num in Number.manager().all()}
        excel.worksheet.write_column(0, 0, data)
        excel.close()

        self.bot.send_document(
            pm.chat.id, open(excel.file_path, 'rb'), pm.message_id,
            InfoMessages.EXPORT_CAPTION.format(count=len(data))
        )

    def handle_manage_number(self, pm: Message, handler: Callable):
        """Add or Remove number to/from database"""
        msg = self.bot.reply_to(
            pm,
            InfoMessages.INPUT_NUMBER.format(example=AddNumberValidator.example)
        )
        self.bot.register_next_step_handler(msg, handler)

    def next_handler_add_number(self, pm: Message):
        """Next step for add number to database"""
        validated_number = AddNumberValidator.validate(pm)

        number = Number(number=validated_number).save()
        self.bot.reply_to(
            pm,
            InfoMessages.ADD_NUMBER_SUCCESS.format(number=number.number),
            reply_markup=self.markup
        )

    def next_handler_delete_number(self, pm: Message):
        """Next step for delete number from database"""
        validated_number = DeleteNumberValidator.validate(pm)

        number = Number.manager().get(number=validated_number)
        number.delete()
        self.bot.reply_to(
            pm,
            InfoMessages.DELETE_NUMBER_SUCCESS.format(number=number.number),
            reply_markup=self.markup
        )

    def run(self):
        print("Bot started.")
        self.bot.infinity_polling()

    @property
    def markup(self):
        """Return keyboard markup"""
        mk = types.ReplyKeyboardMarkup(True, True, row_width=1)
        mk.add(ButtonTexts.ADD_NUMBER)
        mk.add(ButtonTexts.EXPORT)
        mk.add(ButtonTexts.DEL_NUMBER)
        return mk
