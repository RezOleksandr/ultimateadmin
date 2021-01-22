# -*- coding: utf-8 -*-

commands_list = ['/start', '/help', 'me', 'language', '/add_admin', 'Add admin', 'Додати адміна', 'Добавить админа',
                 '/promote', 'Promote', 'Повисити', 'Повысить', '/demote', 'Demote', 'Понизити', 'Понизить', '/pin',
                 'Pin', 'Пін', 'Закріпити', 'Пин', 'Закрепить', '/silent_pin', 'Silent pin', 'Тихий пін',
                 'Тихо закріпити', 'Тихий пин', 'Тихо закрепить', '/readonly', 'Readonly', 'RO', 'Ro', 'Рідонлі',
                 'РО', 'Ро', 'Ридонли', '/restrict_media', 'Restrict media', 'Ban media', 'Обмежити медіа',
                 'Бан медіа', 'Ограничить медиа', 'Бан медиа', '/kick', 'Kick', 'Кік', 'Кик', '/ban', 'Ban', 'Бан',
                 '/unban', 'Unban', 'Розблокувати',  'Разблокировать']

back = [
    {
        'en': 'Back',
        'ua': 'Назад',
        'ru': 'Назад'
    }
]

error = [
    {
        'en': 'Error',
        'ua': 'Помилка',
        'ru': 'Ошибка'
    },
]

help_responses = [
    {
        'en': 'Commands list:',
        'ua': 'Список команд:',
        'ru': 'Список команд:'
    },
    {
        'en': "/start &lt;language(optional)>\nExample: /start ; /start en\nThis command activates the bot in this"
              " chat, can be used to select the bot's language",
        'ua': '/start &lt;мова(необов`язково)>\nПриклад: /start ; /start en\nЦя команда активує бота у цьому чаті, '
              'може бути використана для вибору мови бота',
        'ru': '/start &lt;язык(неабязательно)>\nПример: /start ; /start en\nЭта команда активирует бота в этом чате, '
              'может быть использована для выбора языка бота'
    },
    {
        'en': '/help\nThis command shows the help menu with descriptions of all commands',
        'ua': '/help\nЦя команда показує меню допомоги з описами всіх команд',
        'ru': '/help\nЭта команда показывает меню поможи с описаниями всех команд'
    },
    {
        'en': '/me\nThis command shows information about the user',
        'ua': '/me\nЦя команда показує інформацію про користувача',
        'ru': '/me\nЭта команда показывает информацию про пользователя'
    },
    {
        'en': "/language &lt;language>\nThis command changes bot's language",
        'ua': '/language &lt;мова>\nЦя команда змінює мову бота',
        'ru': '/language &lt;язык>\nЭта команда меняет язык бота'
    },
    {
        'en': "/add_admin\nReply to the user's message with this command to give him admin rights in the bot. To use th"
              'is command you must be the owner of this chat or be an admin with permission to appoint new admins'
              '\nAlternative forms: <b>Add admin</b>',
        'ua': '/add_admin\nВідповідайте на повідомлення користувача цією командою, щоб надати йому права адміністрата у'
              ' боті. Щоб використовувати цю команду ви маєте бути власником цього чату або бути адміністратором, який'
              ' має дозвіл призначати нових адміністраторів\nАльтернативні форми: <b>Додати адміна</b>',
        'ru': '/add_admin\nОтвечайте на сообщения пользователей этой командой, чтобы дать ему права администрато в бот'
              'е. Чтобы использовать эту команду вы должны быть владельцем этого чата или быть администратором, котор'
              'ый имеет разрешение назначать новых администраторов\nАльтернативные формы: <b>Добавить админа</b>'
    },
    {
        'en': "/promote\nReply to the user's message with this command to increase his level of rights in the bot. To u"
              'se this command you must be the owner of this chat, be an admin with permission to appoint new admins or'
              ' have a higher level of rights than the targeted user\nAlternative forms: <b>Promote</b>',
        'ua': '/promote\nВідповідайте на повідомлення користувача цією командою, щоб надати йому більше прав у боті. '
              'Щоб використовувати цю команду ви маєте бути власником цього чату, бути адміністратором який має дозвіл '
              'призначати нових адміністраторів або мати більший рівень прав ніж цільовий користувач'
              '\nАльтернативні форми: <b>Повисити</b>',
        'ru': '/promote\nОтвечайте на сообщения пользователя этой командой, чтобы предоставить ему больше прав в боте.'
              ' Чтобы использовать эту команду вы должны быть владельцем этого чата, быть администратором который имее'
              'т разрешение назначать новых администраторов или иметь больший уровень прав чем целевой пользователь'
              '\nАльтернативные формы: <b>Повысить</b>'
    },
    {
        'en': "/demote\nReply to the user's message with this command to lower his level of rights rights in the bot. T"
              'o use this command you must be the owner of this chat, be an admin with permission to appoint new admins'
              ' or have a higher level of rights than the targeted user\nAlternative forms: <b>Demote</b>',
        'ua': '/demote\nВідповідайте на повідомлення користувача цією командою, щоб зменшити його рівнь прав у боті. '
              'Щоб використовувати цю команду ви маєте бути власником цього чату, бути адміністратором який має дозвіл '
              'призначати нових адміністраторів або мати більший рівень прав ніж цільовий користувач'
              '\nАльтернативні форми: <b>Понизити</b>',
        'ru': '/demote\nОтвечайте на сообщения пользователя этой командой, чтобы уменьшить его уровень прав прав в бо'
              'те. Чтобы использовать эту команду вы должны быть владельцем этого чата, администратором который им'
              'еет разрешение назначать новых администраторов или иметь больший уровень прав чем целевой пользователь'
              '\nАльтернативные формы: <b>Понизить</b>'
    },
    {
        'en': '/pin\nReply to the message with this command to pin it. To use this command you must be the owner of thi'
              's chat, be an admin with permission to pin messages or have a rights level in the bot higher than 1'
              '\nAlternative forms: <b>Pin</b>',
        'ua': '/pin\nВідповідайте на повідомлення цією командою, щоб закріпити його. Щоб використовувати цю ком'
              'анду ви маєте бути власником цього чату, бути адміністратором який має дозвіл закріплювати повідомле'
              'ння або мати рівень прав у боті більше 1\nАльтернативні форми: <b>Пін</b>, <b>Закріпити</b>',
        'ru': '/pin\nОтвечайте на сообщение этой командой, чтобы закрепить его. Чтобы использовать эту команду вы до'
              'лжны быть владельцем этого чата, администратором который имеет разрешение закреплять сообщения или иметь'
              'уровень прав в боте больше 1\nАльтернативные формы: <b>Пин</b>, <b>Закрепить</b>'
    },
    {
        'en': '/silent_pin\nReply to the message with this command to pin it without notifications. To use this comm'
              'and you must be the owner of this chat, be an admin with permission to pin messages or have a rights '
              'level in the bot higher than 1\nAlternative forms: <b></b>',
        'ua': '/silent_pin\nВідповідайте на повідомлення цією командою щоб закріпити його без сповіщень. Щоб вико'
              'ристовувати цю команду ви маєте бути власником цього чату, бути адміністратором який має дозвіл закріп'
              'лювати повідомлення або мати рівень прав у боті більше 1\nАльтернативні форми: <b>Тихий пін</b>, '
              '<b>Тихо закріпити</b>',
        'ru': '/silent_pin\nОтвечайте на сообщение этой командой чтобы закрепить его без уведомлений. Чтобы использов'
              'ать эту команду вы должны быть владельцем этого чата, администратором который имеет разрешение закреп'
              'лять сообщения или иметь уровень прав в боте больше 1\nАльтернативные формы: <b>Тихий пин</b>, '
              '<b>Тихо закрепить</b>'
    },
    {
        'en': "/readonly &lt;duration&gt;&lt;time measurement units(m|h|d for minutes|hours|days)&gt;\nReply to the"
              " user's message with this command to restrict him from sending any messages."
              " To use this command you must be the owner of this chat, be an admin with permission to ban users or"
              " have rights level 2 in the bot. The owner of this chat, admins and users with admin rights in the"
              " bot cannot be banned\nAlternative forms: <b>Readonly</b>, <b>RO</b>, <b>Ro</b>",
        'ua': '/readonly &lt;тривалість&gt;&lt;одиниці виміру часу(хв|год|д сокращено от хвилини|години|дні)&gt;\n'
              'Відповідайте на повідомлення користувача цією командою, щоб заборонити йому надсилати будь'
              '-які повідомлення. Щоб використовувати цю команду ви маєте бути власником цього чату, бути адміністра'
              'тором який має дозвіл блокувати користувачів або мати рівень прав у боті більше 2. Власник чату,'
              ' адміністратори та користувачі із правами адміністратора у боті не можуть бути заблокованими'
              '\nАльтернативні форми: <b>Рідоноі</b>, <b>РО</b>, <b>Ро</b>',
        'ru': '/readonly &lt;длительность&gt;&lt;единицы измерения времени(м|ч|д сокращено от минуты|часы|дни)&gt;\n'
              'Отвечайте на сообщения пользователя этой командой, чтобы запретить ему отправлять любые '
              'сообщения. Чтобы использовать эту команду вы должны быть владельцем этого чата, администратором'
              ' который имеет разрешение блокировать пользователей или иметь уровень прав в боте больше 2. Владелец '
              'чата, администраторы и пользователи с правами администратора в боте не могут быть заблокированы'
              '\nАльтернативные формы: <b>Ридонли</b>, <b>РО</b>, <b>Ро</b>'
    },
    {
        'en': "/restrict_media &lt;duration&gt;&lt;time measurement units(m|h|d for minutes|hours|days)&gt;\nReply to "
              "the user's message with this command to restrict him from sending any messages other than text. To"
              " use this command you must be the owner of this chat, be an admin with permission to ban users or have"
              " rights level 2 in the bot. The owner of this chat, admins and users with admin rights in the bot cannot"
              " be banned\nAlternative forms: <b>Restrict media</b>, <b>Ban media</b>",
        'ua': '/restrict_media &lt;тривалість&gt;&lt;одиниці виміру часу(хв|год|д сокращено от хвилини|години|дні)&gt;'
              '\nВідповідайте на повідомлення користувача цією командою, щоб заборонити йому надсилати'
              ' будь-які повідомлення крім текстових. Щоб використовувати цю команду ви маєте бути власником цього'
              ' чату, бути адміністратором який має дозвіл блокувати користувачів або мати рівень прав у боті більше'
              ' 2. Власник чату, адміністратори та користувачі із правами адміністратора у боті не можуть бути'
              ' заблокованими\nАльтернативні форми: <b>Обмежити медіа</b>, <b>Бан медіа</b>',
        'ru': '/restrict_media &lt;длительность&gt;&lt;единицы измерения времени(м|ч|д сокращено от минуты|часы|дни)'
              '&gt;\nОтвечайте на сообщения пользователя этой командой, чтобы запретить ему отправлять '
              'любые сообщения кроме текстовых. Чтобы использовать эту команду вы должны быть владельцем этого чата, '
              'администратором который имеет разрешение блокировать пользователей или иметь уровень прав в боте'
              ' больше 2. Владелец чата, администраторы и пользователи с правами администратора в боте не могут быть'
              ' заблокированы\nАльтернативные формы: <b>Ограничить медиа</b>, <b>Бан медиа</b>'
    },
    {
        'en': "/kick\nReply to the user's message with this command to kick him from this chat without ban on"    
              " returning. To use this command you must be the owner of this chat, be an admin with permission to"
              " ban users or have rights level 3 in the bot. The owner of this chat, admins and users with admin"
              " rights in the bot cannot be banned\nAlternative forms: <b>Kick</b>",
        'ua': '/kick\nВідповідайте на повідомлення користувача цією командою, щоб вигнати його із чату без заборони'    
              ' на повернення. Щоб використовувати цю команду ви маєте бути власником цього чату, бути адміністратором'
              ' який має дозвіл блокувати користувачів або мати рівень прав у боті більше 3. Власник чату,'
              ' адміністратори та користувачі із правами адміністратора у боті не можуть бути заблокованими'
              '\nАльтернативні форми: <b>Кік</b>',
        'ru': '/kick\nОтвечайте на сообщения пользователя этой командой, чтобы выгнать его из чата без запрета на'    
              ' возвращение. Чтобы использовать эту команду вы должны быть владельцем этого чата, администратором'
              ' который имеет разрешение блокировать пользователей или иметь уровень прав в боте больше 3. '
              'Владелец чата, администраторы и пользователи с правами администратора в боте не могут быть'
              ' заблокированы\nАльтернативные формы: <b>Кик</b>'
    },
    {
        'en': "/ban\nReply to the user's message with this command to ban him from this chat. To use this command"
              " you must be the owner of this chat, be an admin with permission to ban users or have rights level 3 "
              "in the bot. The owner of this chat, admins and users with admin rights in the bot cannot be banned"
              "\nAlternative forms: <b>Ban</b>",
        'ua': '/ban\nВідповідайте на повідомлення користувача цією командою, щоб забанити його у цьому чаті. Щоб'
              ' використовувати цю команду ви маєте бути власником цього чату, бути адміністратором'
              ' який має дозвіл блокувати користувачів або мати рівень прав у боті більше 3. Власник чату,'
              ' адміністратори та користувачі із правами адміністратора у боті не можуть бути заблокованими'
              '\nАльтернативні форми: <b>Бан</b>',
        'ru': '/ban\nОтвечайте на сообщения пользователя этой командой, чтобы забанить его в этом чате. Чтобы'
              ' использовать эту команду вы должны быть владельцем этого чата, администратором'
              ' который имеет разрешение блокировать пользователей или иметь уровень прав в боте больше 3. '
              'Владелец чата, администраторы и пользователи с правами администратора в боте не могут быть'
              ' заблокированы\nАльтернативные формы: <b>Бан</b>'
    },
    {
        'en': "/unban\nReply to the user's message with this command to lift all restrictions off him. To use this"
              " command you must be the owner of this chat, be an admin with permission to ban users or have rights"
              " level 2 in the bot\nAlternative forms: <b>Unban</b>",
        'ua': '/unban\nВідповідайте на повідомлення користувача цією командою, щоб зняти з нього всі обмеження. Щоб'
              ' використовувати цю команду ви маєте бути власником цього чату, бути адміністратором'
              ' який має дозвіл блокувати користувачів або мати рівень прав у боті більше 2'
              '\nАльтернативні форми: <b>Розблокувати</b>',
        'ru': '/unban\nОтвечайте на сообщения пользователя этой командой, чтобы снять с него все ограничения. Чтобы'
              ' использовать эту команду вы должны быть владельцем этого чата, администратором'
              ' который имеет разрешение блокировать пользователей или иметь уровень прав в боте больше 2'
              '\nАльтернативные формы: <b>Разблокировать</b>'
    },
]

me_responses = [
    {
        'en': 'ID: {}\nUsername: @{}\nRights: {}',
        'ua': 'ID: {}\nUsername: @{}\nПрава: {}',
        'ru': 'ID: {}\nUsername: @{}\nПрава: {}'
    },
]

inline_language_selection_responses = [
    {
        'en': 'Chose language:',
        'ua': 'Оберіть мову:',
        'ru': 'Выберите язык:'
    },
    {
        'en': 'Language is already set to english',
        'ua': 'Мова вже встановлена на українську',
        'ru': 'Язык уже установлен на русский'
    },
    {
        'en': 'Language switched to english',
        'ua': 'Мову змінено на українську',
        'ru': 'Язык изменен на русский'
    },
]

add_admin_responses = [
    {
        'en': 'Assignment is successful',
        'ua': 'Призначення успішне',
        'ru': 'Назначение упешно'
    },
]

promote_responses = [
    {
        'en': 'Maximum level of rights (3)',
        'ua': 'Максимальний рівень прав (3)',
        'ru': 'Максимальный уровень прав (3)'
    },
    {
        'en': 'Rights level is increased to {}',
        'ua': 'Рівень прав повишено до {}',
        'ru': 'Уровень прав повышен до {}'
    },
]

demote_responses = [
    {
        'en': 'Minimum level of rights (0)',
        'ua': 'Мінімальний рівень прав (0)',
        'ru': 'Минимальный уровень прав (0)'
    },
    {
        'en': 'Rights level is decreased to {}',
        'ua': 'Рівень прав понижено до {}',
        'ru': 'Уровень прав понижен до {}'
    },
]

readonly_responses = [
    {
        'en': 'User is restricted for {}{}',
        'ua': 'Користувача обмежено на {}{}',
        'ru': 'Пользователь ограничен на {}{}'
    },
    {
        'en': 'm',
        'ua': 'хв',
        'ru': 'м'
    },
    {
        'en': 'h',
        'ua': 'год',
        'ru': 'ч'
    },
    {
        'en': 'd',
        'ua': 'д',
        'ru': 'д'
    },
]

kick_responses = [
    {
        'en': 'User is kicked from chat',
        'ua': 'Користувача кікнуто з чата',
        'ru': 'Пользователь кикнут из чата'
    },
]

ban_responses = [
    {
        'en': 'User is banned',
        'ua': 'Користувача забанено',
        'ru': 'Пользователь забанен'
    },
]

unban_responses = [
    {
        'en': 'User is unbanned',
        'ua': 'Користувача розблоковано',
        'ru': 'Пользователь разблокирован'
    },
]

not_active_chat_responses = [
    {
        'en': 'Chat is not active, use command /start <en/ua/ru> to activate chat',
        'ua': 'Чат не активний, використайте команду /start <en/ua/ru> для активації',
        'ru': 'Чат не активен, используйте команду /start <en/ua/ru> для активации'
    },
]

unknown_inline_query = [
    {
        'en': 'Button is not active',
        'ua': 'Кнопка не активна',
        'ru': 'Кнопка не активна'
    },
]
