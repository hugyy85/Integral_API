import user
from db.operations import _exit
import config


def main(auth_user):
    while True:
        print(auth_user)
        print('''
                Чтобы изменить ФИО введите 1
                Чтобы изменить пол введите 2
                Чтобы изменить пароль введите 3
                Чтобы изменить номер телефона введите 4
                Чтобы изменить email введите 5
                Чтобы выйти введите 0
                '''
              )
        answer = input('Введите число: ')

        if answer == '1':
            auth_user.name = user.change_name(auth_user.id)
        elif answer == '2':
            auth_user.gender = user.change_gender(auth_user.id)
        elif answer == '3':
            user.change_password(auth_user.id)
        elif answer == '4':
            auth_user.number = user.change_number(auth_user.id)
        elif answer == '5':
            auth_user.email = user.change_email(auth_user.id)
        elif answer == '0':
            config.log.info(f'Пользователь с именем {auth_user.name} вышел')
            _exit()
