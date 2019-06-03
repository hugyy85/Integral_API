import db.operations
import peewee
import random
import user
import config


def main(message=None):

    # registration new user.
    while True:
        
        # block info.
        print("Регистрация нового пользователя")
        name = input('Введите ФИО: ')

        # choice user gender
        gender = user.change_gender()

        # block password.
        while True:
            password = input('Придумайте пароль: ')
            hsh = db.operations.check_password(password)
            if hsh:
                break

        number = input('Введите номер телефона: ')
        email = input('Введите email: ')

        # write in database information.
        db.operations.connection()
        try:
            db.operations.add_user(name, gender, hsh, number, email)
            print(f'Регистрация пользователя с номером {number} прошла успешно')

        except peewee.IntegrityError as px:
            print(f'\n{px}\n')
            config.log.exception('PEEWEE')
        break


def recovery_password(recovery_email=None, bot=False):
    # block of recovery password
    if not bot:
        print('Вы находитесь в форме восстановления пароля')
        recovery_email = input('Введите email и на него будет отправлен код для восстановления пароля')

    # if user in database, script send email to user_email with verifiable number
    if db.operations.find_user(email=recovery_email):
        recover_id = db.operations.find_user(email=recovery_email)[0]
        verify_code = str(random.randint(100, 10000))
        db.operations.send_email(recovery_email, verify_code)
        # check verifiable number
        if not bot:
            while True:
                code = input('Введите код из email сообщения:')
                if code == verify_code:
                    return recover_id
                print('Не верно, попробуйте снова')
        elif bot:
            return recover_id, verify_code

    else:
        return False







