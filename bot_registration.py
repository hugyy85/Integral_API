import telepot
from config import TELEGRAM_TOKEN
from telegram_bot import bot

import registration
import user


def main():
    def handle(msg):
        bot.sendMessage(chat_id,)

        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)

        if content_type == 'text':
            bot.sendMessage(chat_id, '''Здравствуйте,
            чтобы зарегистрировать нового пользователя введите 1
            Чтобы войти введите 2
            Чтобы восстановить пароль введите 3
            Чтобы выйти введите 0
            ''')
        elif msg['text'] == '1':
            bot.sendMessage(chat_id, bot_registration.main())







main()