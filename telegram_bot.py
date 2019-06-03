import telebot
from telebot import apihelper

from config import TELEGRAM_TOKEN, PROXY, log
import db.operations
import registration
import user

from peewee import IntegrityError
import time
import socket


bot = telebot.TeleBot(TELEGRAM_TOKEN)
data = {}

print('listening...')


################################
# block of main menu
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, '''
        Здравствуйте, чтобы зарегистрировать нового пользователя введите 1
        Чтобы войти введите 2
        Чтобы восстановить пароль введите 3
        Чтобы удалить пользователя введите 4
        Чтобы посмотреть всех пользователей в базе введите 5        
        ''')
        bot.register_next_step_handler(message, get_menu)
    else:
        bot.send_message(message.from_user.id, 'Напишите /reg')


def get_menu(message):
    # main menu API
    if message.text == '1':
        bot.send_message(message.from_user.id, 'Как вас зовут?')
        bot.register_next_step_handler(message, set_name)
    elif message.text == '2':
        bot.send_message(message.from_user.id, 'Введите номер телефона или email')
        bot.register_next_step_handler(message, get_auth)
    elif message.text == '3':
        bot.send_message(message.from_user.id, 'Вы находитесь в форме восстановления пароля\n'
                                               'Введите email и на него будет отправлен код для восстановления пароля')
        bot.register_next_step_handler(message, get_recovery)
    elif message.text == '4':
        bot.send_message(message.from_user.id, 'Введите id, или номер телефона или email чтобы выбрать пользователя для удаления')
        bot.register_next_step_handler(message, delete_user)
    elif message.text == '5':
        text = 'id - name - number - email \n'
        result = user.get_all_users()
        for i in result:
            text += str(i) + '\n'
        bot.send_message(message.from_user.id, text)


def get_auth(message):
    # authentication
    auth_user = False

    if message.text.isdigit() and message.text != '/q':
        auth_user = db.operations.find_user(number=message.text)
    else:
        # if user enter a email
        auth_user = db.operations.find_user(email=message.text)

    if auth_user:
        global data
        data = {
               'recover_id': auth_user[0],
               'name': auth_user[1],
               'gender': auth_user[2],
               'password': auth_user[3],
               'number': auth_user[4],
               'email': auth_user[5],
               'auth': False,
        }
        bot.send_message(message.from_user.id, 'Введите пароль')
        bot.register_next_step_handler(message, get_auth_pass)
    elif message.text != '/q':
        bot.send_message(message.from_user.id, 'Данный пользователь не найден, пробуйте снова или введите /q')
        bot.register_next_step_handler(message, get_auth)
    else:
        _quit_func(message)
# end block of main menu
#################################


#################################
# Block for registered users
def get_auth_pass(message):
    # check password function
    try:
        data['auth'] = db.operations.check_password(message.text, data['password'])
    except ValueError:
        data['auth'] = False

    if not data['auth'] and message.text != '/q':
        bot.send_message(message.from_user.id, 'Не верно, попробуйте снова, чтобы выйти введите /q')
        bot.register_next_step_handler(message, get_auth_pass)
    elif message.text == '/q':
        _quit_func(message)
    else:
        log.info(f'Пользователь {data["name"]} вошел в систему')
        bot.send_message(message.from_user.id, f'''Вы вошли {data["name"]}, чтобы изменить ваше имя введите - 1. 
        чтобы изменить пароль введите - 2,
        чтобы изменить телефон введите - 3,
        чтобы изменить email введите - 4,
        чтобы выйти - 0
''')
        bot.register_next_step_handler(message, check_auth_method)


def check_auth_method(message):
    # menu registered user
    if message.text == '1':
        bot.send_message(message.from_user.id, 'Как вас зовут?')
        bot.register_next_step_handler(message, change_name)
    elif message.text == '2':
        bot.send_message(message.from_user.id, 'Введите новый пароль')
        bot.register_next_step_handler(message, get_recovery_pass)

    elif message.text == '3':
        bot.send_message(message.from_user.id, 'Введите новый телефон')
        bot.register_next_step_handler(message, change_number)
    elif message.text == '4':
        bot.send_message(message.from_user.id, 'Введите новый email')
        bot.register_next_step_handler(message, change_email)
    elif message.text == '0':
        bot.send_message(message.from_user.id, f'До свидания {data["name"]}')
        log.info(f'Пользователь {data["name"]} вышел')


def change_number(message):
    user.change_number(data['recover_id'], message.text)
    bot.send_message(message.from_user.id, 'Вы успешно сменили телефон')


def change_email(message):
    user.change_email(data['recover_id'], message.text)
    bot.send_message(message.from_user.id, 'Вы успешно сменили email')


def change_name(message):
    user.change_name(data['recover_id'], message.text)
    data['name'] = message.text
    bot.send_message(message.from_user.id, 'Вы успешно сменили имя')
# end block for registered users
######################################


######################################
# Block registration new user
def set_name(message):
    data['name'] = message.text
    bot.send_message(message.from_user.id, 'Укажите номер телефона')
    bot.register_next_step_handler(message, set_num)


def set_num(message):
    data['number'] = message.text
    bot.send_message(message.from_user.id, 'Укажите email')
    bot.register_next_step_handler(message, set_email)


def set_email(message):
    data['email'] = message.text
    bot.send_message(message.from_user.id, 'Укажите пароль')
    bot.register_next_step_handler(message, set_password)


def set_password(message):
    data['password'] = db.operations.check_password(message.text, bot=bot)
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Муж', callback_data='Муж')
    key_no = telebot.types.InlineKeyboardButton(text='Жен', callback_data='Жен')
    keyboard.add(key_yes, key_no)
    bot.send_message(message.from_user.id, text='Укажите пол', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    data['gender'] = call.data
    try:
        db.operations.add_user(
                           data['name'],
                           data['gender'],
                           data['password'],
                           data['number'],
                           data['email'],)
        bot.send_message(call.from_user.id, 'Вы зарегистрированы, чтобы войти введите /reg')
    except IntegrityError as px:
        print(f'\n{px}\n')
        bot.send_message(call.from_user.id, f'Вы не зарегистрированы, так как \n{px}\n')

    print(data)
# end block registration
#####################################


#####################################
# Block for other functions
def delete_user(message):
    # delete user from database if you know id or number, or email
    if message.text == '/q':
        _quit_func(message)
    result = user.delete_user(message.text)
    if not result:
        bot.send_message(message.from_user.id, 'Такого юзера не существует, поробуй еще раз или напиши /q')
        bot.register_next_step_handler(message, delete_user)
    else:
        bot.send_message(message.from_user.id, result)


def get_recovery(message):
    # change password function
    # check verify cod from email
    if message.text.isdigit():
        if message.text == data.get('verify_code'):
            bot.send_message(message.from_user.id, f'Введите новый пароль')
            bot.register_next_step_handler(message, get_recovery_pass)
    else:
        recover_id, verify_code = registration.recovery_password(message.text, bot=True)
        bot.send_message(message.from_user.id, 'Введите код из email')
        data['recover_id'] = recover_id
        data['verify_code'] = verify_code
        bot.register_next_step_handler(message, get_recovery)


def get_recovery_pass(message):
    # change password in database
    user.change_password(data['recover_id'], message.text, bot=True)
    bot.send_message(message.from_user.id, f'Вы успешно сменили пароль')


def find_proxy(proxy_file='proxy.txt'):
    # return list of proxies
    proxy = ''
    with open(proxy_file, 'r') as f:
        proxy = f.read()
    return proxy.split('\n')


def _quit_func(message):
    # function to quit from loop
    bot.send_message(message.from_user.id, 'Чтобы выйти в главное меню введите /reg')
    bot.register_next_step_handler(message, start)

# end block for other functions
###########################################


# enumeration proxies from 1.txt or change PROXY in config.py
if __name__ == '__main__':
    if PROXY:
        while True:
            time.sleep(2)
            try:
                apihelper.proxy = {'https': f'http://{PROXY}'}
                bot.polling()
            except:
                log.exception('TELEGRAM_ERR')

    elif not PROXY:
        proxy_list = find_proxy()
        for prox in proxy_list:
            time.sleep(1)
            try:
                apihelper.proxy = {'https': f'http://{prox}'}
                bot.polling()
            except:
                log.exception('TELEGRAM_ERR')
                print(f'{prox} does not work, trying next...')

        print('Это лист прокси не работает, нужны новые')



