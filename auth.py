import registration
import user
import db.operations
import config


def auth():

    while True:
        print("Здравствуйте, чтобы зарегистрировать нового пользователя введите 1")
        print("Чтобы войти введите 2")
        print('Чтобы восстановить пароль введите 3')
        input_data = input('Введите число: ')

        if input_data == '1':
            # new user registration
            registration.main()

        elif input_data == '2':
            # authentication user
            data = input('Введите номер телефона или email: ')
            password = input('Введите пароль: ')

            if data.isdigit():
                # if user enter a number
                auth_user = db.operations.find_user(number=data)
            else:
                # if user enter a email
                auth_user = db.operations.find_user(email=data)
            # check password
            if auth_user and db.operations.check_password(password, auth_user[3]):
                text = f'Пользователь с именем {auth_user[1]} вошел в систему'
                print(text)
                config.log.info(text)
                return user.User(auth_user)
            else:
                print('Не верно введен логин или пароль')

        # recovery password
        elif input_data == '3':

            user_id = registration.recovery_password()
            # if user in database, change password
            if user_id:
                user.change_password(user_id)


        # exit
        elif input_data == '0':
            db.operations._exit()

        else:
            print('Не верное значение, попробуйте снова\n')
