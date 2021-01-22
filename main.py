# -*- coding: utf-8 -*-
import logging
import filters
import time
import re
import random

import psycopg2
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Message, ChatMember, CallbackQuery, \
    ChatPermissions
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, CallbackContext

from config import TOKEN, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import texts

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG, stream=open('debug_logs.log', 'a',
                                                                                         encoding='utf-8'))

bot_logger = logging.getLogger("bot_logger")
info_handler = logging.FileHandler('logs.log', encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_format = logging.Formatter('%(asctime)s - %(message)s')
info_handler.setFormatter(info_format)
debug_handler = logging.FileHandler('debug_logs.log', encoding='utf-8')
debug_handler.setLevel(logging.DEBUG)
debug_format = logging.Formatter('%(asctime)s - %(message)s')
debug_handler.setFormatter(debug_format)

bot_logger.addHandler(info_handler)
bot_logger.addHandler(debug_handler)
bot_logger.setLevel(logging.INFO)


def message_log(message: Message, reply: Message) -> None:
    """Processes logs for usual text messages"""

    logging_info_text = 'message: (text: {}, id: {}) | from: (username: {}, id: {} | chat: {} | ' \
                        'reply: (text: {}, chat: (id: {}, first_name: {}) | reply_markup: {}'
    bot_logger.info(logging_info_text.format(message.text, message.message_id, message.from_user.username,
                                             message.from_user.id, message.chat, reply.text, reply.chat.id,
                                             reply.chat.first_name, message.reply_markup))


def inline_callback_log(query: CallbackQuery, query_answer: str) -> None:
    """Processes logs for inline callbacks"""

    message = query.message

    logging_info_text = 'message: (text: {}, id: {}) | from: (username: {}, id: {} | chat: {} | ' \
                        'query_answer: {}, '
    bot_logger.info(logging_info_text.format(message.text, message.message_id, message.from_user.username,
                                             message.from_user.id, message.chat, query_answer))


def has_enough_rights(user_id: int, chat_id: int, rights_needed: int, chat_member: ChatMember,
                      permissions_required: list = None) -> bool:
    """Determines if user has enough rights or permissions for certain action"""

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    curs = conn.cursor()
    curs.execute('SELECT rights FROM admins WHERE user_id = %s AND chat_id = %s', [user_id, chat_id])
    user_rights = curs.fetchone()
    conn.close()

    if user_rights:
        user_rights = user_rights[0]
        if user_rights >= rights_needed:
            return True
    if chat_member:
        if chat_member.status == 'creator':
            return True
        elif chat_member.status == 'administrator' and permissions_required:
            chat_member_permissions = [
                chat_member.can_change_info, chat_member.can_delete_messages, chat_member.can_invite_users,
                chat_member.can_restrict_members, chat_member.can_pin_messages, chat_member.can_promote_members
            ]
            for i in range(0, 6):
                if permissions_required[i] > chat_member_permissions[i]:
                    return False
            return True
    return False


def start(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    curs = conn.cursor()
    curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
    chat = curs.fetchone()
    if not chat:
        if message.chat.type != 'private':
            if context.args:
                if context.args[0] in ['en', 'ru', 'ua']:
                    curs.execute("INSERT INTO chats VALUES (%s,%s,%s,%s)",
                                 [message.chat.id, message.chat.title, context.args[0], True])
            else:
                curs.execute("INSERT INTO chats VALUES (%s,%s,%s,%s)",
                             [message.chat.id, message.chat.title, 'ru', True])
    else:
        if not chat[3]:
            curs.execute("UPDATE chats SET is_active = True WHERE id = %s", [message.chat.id])
        if context.args:
            if context.args[0] in ['en', 'ru', 'ua']:
                curs.execute("UPDATE chats SET language = %s WHERE id = %s", [context.args[0], message.chat.id])
        curs.execute("SELECT name FROM chats WHERE id = %s", [message.chat.id])
        old_name = curs.fetchone()
        if old_name[0] != message.chat.title:
            curs.execute("UPDATE chats SET name = %s WHERE id = %s", [message.chat.title, message.chat.id])
    conn.commit()
    reply = bot.send_message(chat_id=message.chat.id, text='Start')
    message_log(message, reply)
    conn.close()


def bot_help(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    curs = conn.cursor()
    curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
    chat = curs.fetchone()
    conn.close()

    keyboard = [
        [
            InlineKeyboardButton(text='/start', callback_data='command_description_start'),
            InlineKeyboardButton(text='/help', callback_data='command_description_help'),
            InlineKeyboardButton(text='/me', callback_data='command_description_me'),
        ],
        [
            InlineKeyboardButton(text='/language', callback_data='command_description_language'),
            InlineKeyboardButton(text='/add_admin', callback_data='command_description_add_admin'),
            InlineKeyboardButton(text='/promote', callback_data='command_description_promote'),
        ],
        [
            InlineKeyboardButton(text='/demote', callback_data='command_description_demote'),
            InlineKeyboardButton(text='/pin', callback_data='command_description_pin'),
            InlineKeyboardButton(text='/silent_pin', callback_data='command_description_silent_pin'),
        ],
        [
            InlineKeyboardButton(text='/readonly', callback_data='command_description_readonly'),
            InlineKeyboardButton(text='/restrict_media', callback_data='command_description_restrict_media'),
            InlineKeyboardButton(text='/kick', callback_data='command_description_kick'),
        ],
        [
            InlineKeyboardButton(text='/ban', callback_data='command_description_ban'),
            InlineKeyboardButton(text='/unban', callback_data='command_description_unban'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    reply = bot.send_message(chat_id=message.chat.id, text=texts.help_responses[0][chat[2]], reply_markup=reply_markup)
    message_log(message, reply)


def inline_help(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    message = query.message
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    curs = conn.cursor()
    curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
    chat = curs.fetchone()
    conn.close()

    keyboard = [
        [
            InlineKeyboardButton(text='/start', callback_data='command_description_start'),
            InlineKeyboardButton(text='/help', callback_data='command_description_help'),
            InlineKeyboardButton(text='/me', callback_data='command_description_me'),
        ],
        [
            InlineKeyboardButton(text='/language', callback_data='command_description_language'),
            InlineKeyboardButton(text='/add_admin', callback_data='command_description_add_admin'),
            InlineKeyboardButton(text='/promote', callback_data='command_description_promote'),
        ],
        [
            InlineKeyboardButton(text='/demote', callback_data='command_description_demote'),
            InlineKeyboardButton(text='/pin', callback_data='command_description_pin'),
            InlineKeyboardButton(text='/silent_pin', callback_data='command_description_silent_pin'),
        ],
        [
            InlineKeyboardButton(text='/readonly', callback_data='command_description_readonly'),
            InlineKeyboardButton(text='/restrict_media', callback_data='command_description_restrict_media'),
            InlineKeyboardButton(text='/kick', callback_data='command_description_kick'),
        ],
        [
            InlineKeyboardButton(text='/ban', callback_data='command_description_ban'),
            InlineKeyboardButton(text='/unban', callback_data='command_description_unban'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    reply = bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                  text=texts.help_responses[0][chat[2]], reply_markup=reply_markup)
    message_log(message, reply)


def command_description_inline_response(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    bot = context.bot
    message = query.message
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    curs = conn.cursor()

    curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
    chat = curs.fetchone()
    conn.close()

    keyboard = [
        [
            InlineKeyboardButton(text=texts.back[0][chat[2]], callback_data='help'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target_command = re.match(r'command_description_(?P<command>\S+)$', query.data).group('command')
    if target_command == 'start':

        reply_text = texts.help_responses[1][chat[2]]
    elif target_command == 'help':
        reply_text = texts.help_responses[2][chat[2]]
    elif target_command == 'me':
        reply_text = texts.help_responses[3][chat[2]]
    elif target_command == 'language':
        reply_text = texts.help_responses[4][chat[2]]
    elif target_command == 'add_admin':
        reply_text = texts.help_responses[5][chat[2]]
    elif target_command == 'promote':
        reply_text = texts.help_responses[6][chat[2]]
    elif target_command == 'demote':
        reply_text = texts.help_responses[7][chat[2]]
    elif target_command == 'pin':
        reply_text = texts.help_responses[8][chat[2]]
    elif target_command == 'silent_pin':
        reply_text = texts.help_responses[9][chat[2]]
    elif target_command == 'readonly':
        reply_text = texts.help_responses[10][chat[2]]
    elif target_command == 'restrict_media':
        reply_text = texts.help_responses[11][chat[2]]
    elif target_command == 'kick':
        reply_text = texts.help_responses[12][chat[2]]
    elif target_command == 'ban':
        reply_text = texts.help_responses[13][chat[2]]
    elif target_command == 'unban':
        reply_text = texts.help_responses[14][chat[2]]
    else:
        reply_text = texts.error[0][chat[2]]

    try:
        reply = bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                      text=reply_text, reply_markup=reply_markup, parse_mode="HTML")
        message_log(message, reply)
    except telegram.error.BadRequest:
        return


def me(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    curs = conn.cursor()
    curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
    chat = curs.fetchone()
    curs.execute("SELECT * FROM admins WHERE user_id = %s", [message.from_user.id])
    user = curs.fetchone()
    if user:
        reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                 text=texts.me_responses[0][chat[2]].format(message.from_user.id,
                                                                            message.from_user.username, user[3]))
        message_log(message, reply)
    else:
        reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                 text=texts.me_responses[0][chat[2]].format(message.from_user.id,
                                                                            message.from_user.username, 0))
        message_log(message, reply)
    conn.close()


# noinspection PyUnusedLocal
def inline_language_selection(update: Update, context: CallbackContext):
    message = update.message
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    curs = conn.cursor()

    curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
    chat = curs.fetchone()
    conn.close()

    keyboard = [
        [
            InlineKeyboardButton(text='🇷🇺Русский', callback_data='ru'),
            InlineKeyboardButton(text='🇺🇦Українська', callback_data='ua'),
            InlineKeyboardButton(text='🇬🇧English', callback_data='en')
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    reply = message.reply_text(texts.inline_language_selection_responses[0][chat[2]], reply_markup=reply_markup)
    message_log(message, reply)


# noinspection PyUnusedLocal
def language_selection_inline_response(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    bot = context.bot
    message = query.message
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    curs = conn.cursor()

    curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
    chat = curs.fetchone()

    if query.data == chat[2]:
        query.answer(texts.inline_language_selection_responses[1][chat[2]])
        inline_callback_log(query, texts.inline_language_selection_responses[1][chat[2]])
    else:
        curs.execute('UPDATE chats SET language = %s WHERE id = %s', [query.data, message.chat.id])
        conn.commit()
        curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
        chat = curs.fetchone()

        reply = message.reply_text(texts.inline_language_selection_responses[2][chat[2]])
        message_log(message, reply)
        query.answer(texts.inline_language_selection_responses[2][chat[2]])
        inline_callback_log(query, texts.inline_language_selection_responses[2][chat[2]])

        keyboard = [
            [
                InlineKeyboardButton(text='🇷🇺Русский', callback_data='ru'),
                InlineKeyboardButton(text='🇺🇦Українська', callback_data='ua'),
                InlineKeyboardButton(text='🇬🇧English', callback_data='en')
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(texts.inline_language_selection_responses[0][chat[2]], reply_markup=reply_markup)
    conn.close()


def add_admin(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if message.from_user.id == message.reply_to_message.from_user.id:
            return
        if has_enough_rights(message.from_user.id, message.chat.id, 4,
                             bot.getChatMember(message.chat.id, message.from_user.id),
                             [False, False, False, False, False, True]):
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            curs = conn.cursor()
            curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
            chat = curs.fetchone()
            curs.execute('SELECT user_id FROM admins WHERE chat_id = %s', [message.chat.id])
            registered_users = curs.fetchall()
            is_registered = False
            if registered_users:
                for user in registered_users:
                    if message.reply_to_message.from_user.id in user:
                        is_registered = True
            if is_registered:
                curs.execute("UPDATE admins SET username = %s, rights = %s WHERE user_id = %s",
                             [message.reply_to_message.from_user.username, 1, message.reply_to_message.from_user.id])
            else:
                curs.execute(
                    'INSERT INTO admins VALUES (%s,%s,%s,%s)',
                    [message.reply_to_message.from_user.id, message.chat.id,
                     message.reply_to_message.from_user.username, 1]
                )
                reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                         text=texts.add_admin_responses[0][chat[2]])
                message_log(message, reply)
            conn.commit()
            conn.close()


def promote(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if message.from_user.id == message.reply_to_message.from_user.id:
            return
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        curs = conn.cursor()
        curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
        chat = curs.fetchone()
        curs.execute('SELECT * FROM admins WHERE user_id = %s AND chat_id = %s',
                     [message.reply_to_message.from_user.id, message.chat.id])
        target_user = curs.fetchone()
        if target_user:
            if has_enough_rights(message.from_user.id, message.chat.id, target_user[3] + 2,
                                 bot.getChatMember(message.chat.id, message.from_user.id),
                                 [False, False, False, False, False, True]):
                if target_user[3] >= 3:
                    reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                             text=texts.promote_responses[0][chat[2]])
                    message_log(message, reply)
                else:
                    curs.execute("UPDATE admins SET rights = %s WHERE user_id = %s",
                                 [target_user[3] + 1, target_user[0]])

                    reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                             text=texts.promote_responses[1][chat[2]].format(target_user[3] + 1))
                    message_log(message, reply)
                    conn.commit()
        conn.close()


def demote(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if message.from_user.id == message.reply_to_message.from_user.id:
            return
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        curs = conn.cursor()
        curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
        chat = curs.fetchone()
        curs.execute('SELECT * FROM admins WHERE user_id = %s AND chat_id = %s',
                     [message.reply_to_message.from_user.id, message.chat.id])
        target_user = curs.fetchone()
        if target_user:
            if has_enough_rights(message.from_user.id, message.chat.id, target_user[3] + 1,
                                 bot.getChatMember(message.chat.id, message.from_user.id),
                                 [False, False, False, False, False, True]):
                if target_user[3] <= 0:
                    reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                             text=texts.demote_responses[0][chat[2]])
                    message_log(message, reply)
                else:
                    curs.execute("UPDATE admins SET rights = %s WHERE user_id = %s",
                                 [target_user[3] - 1, target_user[0]])

                    reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                             text=texts.demote_responses[1][chat[2]].format(target_user[3] - 1))
                    message_log(message, reply)
                    conn.commit()
        conn.close()


def pin(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if has_enough_rights(message.from_user.id, message.chat.id, 1,
                             bot.getChatMember(message.chat.id, message.from_user.id),
                             [False, False, False, False, True, False]):
            try:
                bot.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
                logging_info_text = 'message: (text: {}, id: {}) | from: (username: {}, id: {} | chat: {} | ' \
                                    'reply: Pinned message'
                bot_logger.info(logging_info_text.format(message.text, message.message_id, message.from_user.username,
                                                         message.from_user.id, message.chat))
            except telegram.error.BadRequest:
                return


def silent_pin(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if has_enough_rights(message.from_user.id, message.chat.id, 1,
                             bot.getChatMember(message.chat.id, message.from_user.id),
                             [False, False, False, False, True, False]):
            try:
                bot.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id,
                                     disable_notification=True)
                logging_info_text = 'message: (text: {}, id: {}) | from: (username: {}, id: {} | chat: {} | ' \
                                    'reply: Pinned message'
                bot_logger.info(logging_info_text.format(message.text, message.message_id, message.from_user.username,
                                                         message.from_user.id, message.chat))
            except telegram.error.BadRequest:
                return


def readonly(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if message.from_user.id == message.reply_to_message.from_user.id:
            return
        if has_enough_rights(message.from_user.id, message.chat.id, 2,
                             bot.getChatMember(message.chat.id, message.from_user.id),
                             [False, False, False, True, False, False]):
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            curs = conn.cursor()
            curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
            chat = curs.fetchone()
            curs.execute('SELECT * FROM admins WHERE user_id = %s AND chat_id = %s',
                         [message.reply_to_message.from_user.id, message.chat.id])
            target_user = curs.fetchone()
            conn.close()
            target_user_chat_member = bot.getChatMember(message.chat.id, message.reply_to_message.from_user.id)
            if target_user_chat_member.status == 'creator' or target_user_chat_member.status == 'admin':
                return
            if target_user:
                if target_user[3] >= 1:
                    return
            restrictions = ChatPermissions(can_send_messages=False)
            try:
                for command in ['Readonly', 'RO', 'Ro', 'Рідонлі', 'РО', 'Ро', 'Ридонли', '/readonly']:
                    if message.text == command:
                        bot.restrict_chat_member(
                            chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                            permissions=restrictions, until_date=int(time.time() + 300))

                        reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                                 text=texts.readonly_responses[0][chat[2]].format(
                                                     5, texts.readonly_responses[1][chat[2]]))
                        message_log(message, reply)
                        return
                    elif re.match(r'{0}\s\d+[mhdгмчд]$|{0}\s\d+хв$'.format(command), message.text):
                        match = re.match(
                            r'{0}\s(?P<time>\d+)(?P<type>[mhdмчд])$|{0}\s(?P<time2>\d+)(?P<type2>хв)$'.format(command),
                            message.text)

                        restriction_type = match.group('type')
                        if not restriction_type:
                            restriction_type = match.group('type2')

                        restriction_time_number = match.group('time')
                        if not restriction_time_number:
                            restriction_time_number = match.group('time2')
                        restriction_time_number = int(restriction_time_number)

                        restriction_time = 300
                        if restriction_type in ['m', 'хв', 'м']:
                            restriction_time = restriction_time_number * 60
                            restriction_type = texts.readonly_responses[1][chat[2]]
                        elif restriction_type in ['h', 'ч', 'г']:
                            restriction_time = restriction_time_number * 60 * 60
                            restriction_type = texts.readonly_responses[2][chat[2]]
                        elif restriction_type in ['d', 'д']:
                            restriction_time = restriction_time_number * 60 * 60 * 24
                            restriction_type = texts.readonly_responses[3][chat[2]]

                        bot.restrict_chat_member(
                            chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                            permissions=restrictions, until_date=int(time.time() + restriction_time))

                        reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                                 text=texts.readonly_responses[0][chat[2]].format(
                                                     restriction_time_number, restriction_type))
                        message_log(message, reply)
                        return
            except telegram.error.BadRequest:
                return


def restrict_media(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if message.from_user.id == message.reply_to_message.from_user.id:
            return
        if has_enough_rights(message.from_user.id, message.chat.id, 2,
                             bot.getChatMember(message.chat.id, message.from_user.id),
                             [False, False, False, True, False, False]):
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            curs = conn.cursor()
            curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
            chat = curs.fetchone()
            curs.execute('SELECT * FROM admins WHERE user_id = %s AND chat_id = %s',
                         [message.reply_to_message.from_user.id, message.chat.id])
            target_user = curs.fetchone()
            conn.close()
            target_user_chat_member = bot.getChatMember(message.chat.id, message.reply_to_message.from_user.id)
            if target_user_chat_member.status == 'creator' or target_user_chat_member.status == 'admin':
                return
            if target_user:
                if target_user[3] >= 1:
                    return
            restrictions = ChatPermissions(can_send_messages=True)
            try:
                for command in ['Restrict media', 'Ban media', 'Обмежити медіа', 'Бан медіа', 'Ограничить медиа',
                                'Бан медиа', '/restrict_media']:
                    if message.text == command:
                        bot.restrict_chat_member(
                            chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                            permissions=restrictions, until_date=int(time.time() + 300))

                        reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                                 text=texts.readonly_responses[0][chat[2]].format(
                                                     5, texts.readonly_responses[1][chat[2]]))
                        message_log(message, reply)
                        return
                    elif re.match(r'{0}\s\d+[mhdгмчд]$|{0}\s\d+хв$|{0}\s\d+год$'.format(command), message.text):
                        match = re.match(
                            r'{0}\s(?P<time>\d+)(?P<type>[mhdмчд])$|{0}\s(?P<time2>\d+)(?P<type2>хв)$|'
                            r'{0}\s(?P<time3>\d+)(?P<type3>год)$'.format(command),
                            message.text)

                        restriction_type = match.group('type')
                        if not restriction_type:
                            restriction_type = match.group('type2')
                            if not restriction_type:
                                restriction_type = match.group('type3')

                        restriction_duration = match.group('time')
                        if not restriction_duration:
                            restriction_duration = match.group('time2')
                            if not restriction_duration:
                                restriction_duration = match.group('time3')
                        restriction_duration = int(restriction_duration)

                        if restriction_type in ['m', 'хв', 'м']:
                            restriction_duration_final = restriction_duration * 60
                            restriction_type = texts.readonly_responses[1][chat[2]]
                        elif restriction_type in ['h', 'ч', 'год']:
                            restriction_duration_final = restriction_duration * 60 * 60
                            restriction_type = texts.readonly_responses[2][chat[2]]
                        elif restriction_type in ['d', 'д']:
                            restriction_duration_final = restriction_duration * 60 * 60 * 24
                            restriction_type = texts.readonly_responses[3][chat[2]]
                        else:
                            restriction_duration_final = 300

                        bot.restrict_chat_member(
                            chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                            permissions=restrictions, until_date=int(time.time() + restriction_duration_final))

                        reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                                 text=texts.readonly_responses[0][chat[2]].format(
                                                     restriction_duration, restriction_type))
                        message_log(message, reply)
                        return
            except telegram.error.BadRequest:
                return


def kick(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if message.from_user.id == message.reply_to_message.from_user.id:
            return
        if has_enough_rights(message.from_user.id, message.chat.id, 3,
                             bot.getChatMember(message.chat.id, message.from_user.id),
                             [False, False, False, True, False, False]):
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            curs = conn.cursor()
            curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
            chat = curs.fetchone()
            curs.execute('SELECT * FROM admins WHERE user_id = %s AND chat_id = %s',
                         [message.reply_to_message.from_user.id, message.chat.id])
            target_user = curs.fetchone()
            conn.close()
            target_user_chat_member = bot.getChatMember(message.chat.id, message.reply_to_message.from_user.id)
            if target_user_chat_member.status == 'creator' or target_user_chat_member.status == 'admin':
                return
            if target_user:
                if target_user[3] >= 1:
                    return
            try:
                bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
                bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
                reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                         text=texts.kick_responses[0][chat[2]])
                message_log(message, reply)
            except telegram.error.BadRequest:
                return


def ban(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if message.from_user.id == message.reply_to_message.from_user.id:
            return
        if has_enough_rights(message.from_user.id, message.chat.id, 3,
                             bot.getChatMember(message.chat.id, message.from_user.id),
                             [False, False, False, True, False, False]):
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            curs = conn.cursor()
            curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
            chat = curs.fetchone()
            curs.execute('SELECT * FROM admins WHERE user_id = %s AND chat_id = %s',
                         [message.reply_to_message.from_user.id, message.chat.id])
            target_user = curs.fetchone()
            conn.close()
            target_user_chat_member = bot.getChatMember(message.chat.id, message.reply_to_message.from_user.id)
            if target_user_chat_member.status == 'creator' or target_user_chat_member.status == 'admin':
                return
            if target_user:
                if target_user[3] >= 1:
                    return
            try:
                bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
                reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                         text=texts.ban_responses[0][chat[2]])
                message_log(message, reply)
            except telegram.error.BadRequest:
                return


def unban(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.reply_to_message:
        if message.from_user.id == message.reply_to_message.from_user.id:
            return
        if has_enough_rights(message.from_user.id, message.chat.id, 2,
                             bot.getChatMember(message.chat.id, message.from_user.id),
                             [False, False, False, True, False, False]):
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            curs = conn.cursor()
            curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
            chat = curs.fetchone()
            conn.close()
            target_user_chat_member = bot.getChatMember(message.chat.id, message.reply_to_message.from_user.id)
            if target_user_chat_member.status == 'restricted':
                permissions = ChatPermissions(can_send_messages=True, can_send_media_messages=True,
                                              can_send_polls=True, can_send_other_messages=True,
                                              can_add_web_page_previews=True, can_change_info=True,
                                              can_invite_users=True, can_pin_messages=True)
                try:
                    bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                             permissions=permissions)
                    reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                             text=texts.unban_responses[0][chat[2]])
                    message_log(message, reply)
                except telegram.error.BadRequest:
                    return


# noinspection PyUnusedLocal
def no_text(update: Update, context: CallbackContext):
    bot_logger.debug("Message without text")


# noinspection PyUnusedLocal
def not_registered_chat(update: Update, context: CallbackContext):
    pass


# noinspection PyUnusedLocal
def not_active_chat(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.text in texts.commands_list:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        curs = conn.cursor()
        curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
        chat = curs.fetchone()
        reply = bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                 text=texts.not_active_chat_responses[0][chat[2]])
        message_log(message, reply)
        conn.close()


# noinspection PyUnusedLocal
def unknown_inline_query(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    message = query.message
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    curs = conn.cursor()

    curs.execute("SELECT * FROM chats WHERE id = %s", [message.chat.id])
    chat = curs.fetchone()

    query_answer = {'text': texts.unknown_inline_query[0][chat[2]], 'show_alert': True}
    query.answer(text=texts.unknown_inline_query[0][chat[2]], show_alert=True)

    conn.close()


def goose(update: Update, context: CallbackContext):
    message = update.message
    bot = context.bot
    gooses = [
        'AgACAgIAAx0CUP698AACey1f9z6RsT2R_yJUYnrgq64uhmzZfgACw7IxGyvKwUvmmm2Xyl1x0Dcy7ZcuAAMBAAMCAANtAANGVQUAAR4E',
        'AgACAgIAAx0CUP698AACe0Jf9z_KpkgdewH3618XQfFUowHHdwACz7IxGyvKwUuK2vn2CuTapEzmPpYuAAMBAAMCAAN4AANWsgYAAR4E',
        'AgACAgIAAx0CUP698AACe0Nf9z_u9QlEPaBY2fohnr_jGhOqxwAC0LIxGyvKwUv-ecB4j9RBuf3G0pouAAMBAAMCAAN4AANXOQACHgQ',
        'AgACAgIAAx0CUP698AACe0Rf90ABV6k2isiU5IY5RgteEqgHsQAC0bIxGyvKwUv-9K4Z5WrHNrAz7ZcuAAMBAAMCAAN4AANzTgUAAR4E',
        'AgACAgIAAx0CUP698AACe0Vf90AUCsC5hesZpCaYl2TzdRsgxgAC0rIxGyvKwUuREDbvE64QA8ikTJYuAAMBAAMCAAN4AAO4swYAAR4E',
        'AgACAgIAAx0CUP698AACe2Zf90CaXKGvGceysf1x0697houb4gAC2LIxGyvKwUs30O7q6dtGcjz7aZcuAAMBAAMCAANtAAOadgUAAR4E',
        'AgACAgIAAx0CUP698AACe2lf90DaaGYcTK7GM6IpJUMU5Mh7OwAC2bIxGyvKwUvErlqdPDyX1TMQSJYuAAMBAAMCAANtAAN9tgYAAR4E'
    ]
    bot.send_photo(chat_id=message.chat.id, photo=gooses[random.randint(0, 6)])


def main():
    updater = Updater(token=TOKEN, use_context=True, workers=100)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(filters.no_text_filter, no_text, run_async=True))

    dispatcher.add_handler(CommandHandler('start', start, run_async=True))

    dispatcher.add_handler(CommandHandler('help', bot_help, run_async=True))
    dispatcher.add_handler(CallbackQueryHandler(inline_help, pattern=r'help$'))
    dispatcher.add_handler(CallbackQueryHandler(command_description_inline_response, pattern='command_description_'))

    dispatcher.add_handler(MessageHandler(filters.not_registered_chat, not_registered_chat, run_async=True))
    dispatcher.add_handler(MessageHandler(filters.not_active_chat, not_active_chat, run_async=True))

    dispatcher.add_handler(CommandHandler('me', me, run_async=True))

    dispatcher.add_handler(CommandHandler("language", inline_language_selection))
    dispatcher.add_handler(CallbackQueryHandler(language_selection_inline_response, pattern='ua$|ru$|en$'))

    dispatcher.add_handler(MessageHandler(filters.add_admin_filter, add_admin, run_async=True))
    dispatcher.add_handler(CommandHandler('add_admin', add_admin, run_async=True))

    dispatcher.add_handler(MessageHandler(filters.promote_filter, promote, run_async=True))
    dispatcher.add_handler(CommandHandler('promote', promote, run_async=True))
    dispatcher.add_handler(MessageHandler(filters.demote_filter, demote, run_async=True))
    dispatcher.add_handler(CommandHandler('demote', demote, run_async=True))

    dispatcher.add_handler(MessageHandler(filters.pin_filter, pin, run_async=True))
    dispatcher.add_handler(CommandHandler('pin', pin, run_async=True))
    dispatcher.add_handler(MessageHandler(filters.silent_pin_filter, silent_pin, run_async=True))
    dispatcher.add_handler(CommandHandler('silent_pin', silent_pin, run_async=True))

    dispatcher.add_handler(MessageHandler(filters.readonly_filter, readonly, run_async=True))
    dispatcher.add_handler(CommandHandler('readonly', readonly, run_async=True))

    dispatcher.add_handler(MessageHandler(filters.restrict_media_filter, restrict_media, run_async=True))
    dispatcher.add_handler(CommandHandler('restrict_media', restrict_media, run_async=True))

    dispatcher.add_handler(MessageHandler(filters.kick_filter, kick, run_async=True))
    dispatcher.add_handler(CommandHandler('kick', kick, run_async=True))

    dispatcher.add_handler(MessageHandler(filters.ban_filter, ban, run_async=True))
    dispatcher.add_handler(CommandHandler('ban', ban, run_async=True))

    dispatcher.add_handler(MessageHandler(filters.unban_filter, unban, run_async=True))
    dispatcher.add_handler(CommandHandler('unban', unban, run_async=True))

    dispatcher.add_handler(CommandHandler('goose', goose, run_async=True))

    dispatcher.add_handler(CallbackQueryHandler(unknown_inline_query))

    updater.start_polling(timeout=30)


if __name__ == '__main__':
    main()
