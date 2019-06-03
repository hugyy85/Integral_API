import peewee
import pymysql
from db.models import Users, dbhandle
import config
from passlib.hash import pbkdf2_sha256
import smtplib
import os


def _save_row(row):
    # function for save rows in database
    try:
        row.save()
    except peewee.InternalError as px:
        config.log.exception('SAVE_ROW')
        print(str(px))


def add_user(name, gender, password, number, email):
    # adding user in database
    row = Users(
        name=name.lower().strip(),
        gender=gender,
        password=password,
        number=number,
        email=email,
    )
    _save_row(row)
    config.log.info(f'Регистрация пользователя {name} {gender} {password} {number} {email} прошла успешно')


def connection():
    # connection to Mysql
    try:
        dbhandle.close()
    except:
        pass
    dbhandle.connect()


def create_database():
    # creation database
    cursor_type = pymysql.cursors.DictCursor
    connection_instance = pymysql.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        charset='utf8mb4',
        cursorclass=cursor_type
    )

    try:
        cursor_instance = connection_instance.cursor()
        sql_statement = "CREATE DATABASE " + config.db_name
        cursor_instance.execute(sql_statement)
        config.log.info(f'Database {config.db_name} created')

    except Exception as e:
        print("Exception occured:{}".format(e))

    finally:
        connection_instance.close()


def create_tables():
    # creation tables in database
    try:
        connection()
        Users.create_table()
    except peewee.InternalError as px:
        config.log.exception('PEEWEE_CREATE_TABLES')
        print(str(px))


def find_user(number=None, email=None):
    # finding user in database with number or email
    # function return info about found user, or False
    nick_exist = True
    query = ''
    try:
        if number:
            query = Users.select().where(Users.number == number.lower().strip()).get()
        elif email:
            query = Users.select().where(Users.email == email.lower().strip()).get()
    except peewee.DoesNotExist:
        nick_exist = False
        print('Данного пользователя нет в системе')
        return False

    if nick_exist:
        return (query.id, query.name, query.gender, query.password, query.number, query.email, query.date_creation)


def check_password(password=None, hsh=None, bot=False):
    # make new password to new user
    if password and not hsh:
        if bot:
            hsh = pbkdf2_sha256.hash(password)
            return hsh
        else:
            hsh = pbkdf2_sha256.hash(password)
            check = input("Введите пароль еще раз: ")
        if pbkdf2_sha256.verify(check, hsh):
            return hsh
        else:
            return False
    # check password from user
    elif hsh and not password:
        check = input("Введите пароль: ")
        if pbkdf2_sha256.verify(check, hsh):
            return True
        else:
            print("Не верно введен пароль, попробуйте снова")
            return False
    # verification user to enter in API
    elif password and hsh:
        return pbkdf2_sha256.verify(password, hsh)


def send_email(email, message=None):
    smtpObj = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    smtpObj.login('integral.smp123@mail.ru', 'lkjhgfdsa741852963')
    smtpObj.sendmail('integral.smp123@mail.ru', email, message)


def _exit():
    print('До новых встреч!')
    os._exit(0)
