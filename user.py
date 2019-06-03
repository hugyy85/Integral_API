import db.operations
from db.models import Users
import config


class User:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.gender = data[2]
        self.hash_pass = data[3]
        self.number = data[4]
        self.email = data[5]
        self.date_creation = data[6]
        self.auth = True

    def __str__(self):
        return f'id={self.id} {self.name} {self.gender} num={self.number} email={self.email} created at {self.date_creation}'


#####################################
# Block, where changing user info in database
def change_password(user_id, new_pass=None, bot=False):
    # changing password of user with user_id
    if not new_pass:
        new_pass = input('Введите новый пароль: ')
    hsh = db.operations.check_password(password=new_pass, bot=bot)
    query = Users.update({Users.password: hsh}).where(Users.id == user_id)
    query.execute()
    config.log.info(f'id: {user_id} изменил пароль')
    return True


def change_gender(user_id=None):
    while True:
        gender = input("Если вы мужчина введите 1, если женщина 2: ")
        if gender == '1':
            gender = 'Муж'
        elif gender == '2':
            gender = 'Жен'
        else:
            print('Вы ввели некорректные данные, попробуйте снова')
            continue
        break
    if not user_id:
        return gender
    else:
        query = Users.update({Users.gender: gender}).where(Users.id == user_id)
        query.execute()
        config.log.info(f'id: {user_id} изменил пол')
        return gender


def change_name(user_id, name=None):
    if not name:
        name = input('Введите новое ФИО')
    query = Users.update({Users.name: name}).where(Users.id == user_id)
    query.execute()
    config.log.info(f'id: {user_id} изменил имя')
    return name


def change_number(user_id, number=None):
    if not number:
        number = input('Введите новый номер')
    query = Users.update({Users.number: number}).where(Users.id == user_id)
    query.execute()
    config.log.info(f'id: {user_id} изменил номер')
    return number


def change_email(user_id, email=None):
    if not email:
        email = input('Введите новый email')
    query = Users.update({Users.email: email}).where(Users.id == user_id)
    query.execute()
    config.log.info(f'id: {user_id} изменил email')
    return email
#####################################


###########################
# Block telegram_bot API functions
def delete_user(user):
    try:
        query = Users.delete().where(Users.id == user)
        query.execute()
    except:
        try:
            query = Users.delete().where(Users.number == user)
            query.execute()
        except:
            try:
                query = Users.delete().where(Users.email == user)
                query.execute()
            except:
                return False
    if not query:
        return False
    else:
        config.log.info(f'id: {user} deleted')
        return 'Пользователь удален'


def get_all_users():
    # return list of all users in database
    query = Users.select()
    result = []
    for i in query:
        result.append((i.id, i.name, i.number, i.email))
    return result
###########################

