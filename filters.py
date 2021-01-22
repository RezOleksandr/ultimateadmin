from typing import Optional, Union, Dict
import psycopg2
import re

from telegram import Message
from telegram.ext import MessageFilter

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class NoTextFilter(MessageFilter):
    def filter(self, message: Message) -> Optional[Union[bool, Dict]]:
        return message.text is None


no_text_filter = NoTextFilter()


class AddAdminFilter(MessageFilter):
    def filter(self, message: Message) -> Optional[Union[bool, Dict]]:
        for command in ['Add admin', 'Додати адміна', 'Добавить админа']:
            if message.text == command:
                return True
        return False


add_admin_filter = AddAdminFilter()


class PromoteFilter(MessageFilter):
    def filter(self, message: Message) -> Optional[Union[bool, Dict]]:
        for command in ['Promote', 'Повисити', 'Повысить']:
            if message.text == command:
                return True
        return False


promote_filter = PromoteFilter()


class DemoteFilter(MessageFilter):
    def filter(self, message: Message) -> Optional[Union[bool, Dict]]:
        for command in ['Demote', 'Понизити', 'Понизить']:
            if message.text == command:
                return True
        return False


demote_filter = DemoteFilter()


class PinFilter(MessageFilter):
    def filter(self, message: Message) -> Optional[Union[bool, Dict]]:
        for command in ['Pin', 'Пін', 'Закріпити', 'Пин', 'Закрепить']:
            if message.text == command:
                return True
        return False


pin_filter = PinFilter()


class SilentPinFilter(MessageFilter):
    def filter(self, message: Message) -> Optional[Union[bool, Dict]]:
        for command in ['Silent pin', 'Тихий пін', 'Тихо закріпити', 'Тихий пин', 'Тихо закрепить']:
            if message.text == command:
                return True
        return False


silent_pin_filter = SilentPinFilter()


class ReadonlyFilter(MessageFilter):
    def filter(self, message):
        for command in ['Readonly', 'RO', 'Ro', 'Рідонлі', 'РО', 'Ро', 'Ридонли']:
            if re.match(r'{}'.format(command), message.text):
                if message.text == command:
                    return True
                if re.match(r'{0}\s\d+[mhdгмчд]$|{0}\s\d+хв$'.format(command), message.text):
                    return True
        return False


readonly_filter = ReadonlyFilter()


class RestrictMediaFilter(MessageFilter):
    def filter(self, message):
        for command in ['Restrict media', 'Ban media', 'Обмежити медіа', 'Бан медіа', 'Ограничить медиа', 'Бан медиа']:
            if re.match(r'{}'.format(command), message.text):
                if message.text == command:
                    return True
                if re.match(r'{0}\s\d+[mhdгмчд]$|{0}\s\d+хв$'.format(command), message.text):
                    return True
        return False


restrict_media_filter = RestrictMediaFilter()


class KickFilter(MessageFilter):
    def filter(self, message):
        for command in ['Kick', 'Кик', 'Кік']:
            if message.text == command:
                return True
        return False


kick_filter = KickFilter()


class BanFilter(MessageFilter):
    def filter(self, message):
        for command in ['Kick', 'Кик', 'Кік']:
            if message.text == command:
                return True
        return False


ban_filter = BanFilter()


class UnbanFilter(MessageFilter):
    def filter(self, message):
        for command in ['Unban', 'Розблокувати', 'Разблокировать']:
            if message.text == command:
                return True
        return False


unban_filter = UnbanFilter()


class NotRegisteredChat(MessageFilter):
    def filter(self, message: Message) -> Optional[Union[bool, Dict]]:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        curs = conn.cursor()
        curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
        if not curs.fetchone():
            conn.close()
            return True


not_registered_chat = NotRegisteredChat()


class NotActiveChat(MessageFilter):
    def filter(self, message: Message) -> Optional[Union[bool, Dict]]:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        curs = conn.cursor()
        curs.execute("SELECT is_active FROM chats WHERE id = %s", [message.chat.id])
        if not curs.fetchone()[0]:
            conn.close()
            return True


not_active_chat = NotActiveChat()
