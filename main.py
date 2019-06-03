import auth
import db.operations
import main_menu
import config


def main():
    db.operations.create_database()
    db.operations.create_tables()
    while True:
        try:
            authorized_user = auth.auth()
            main_menu.main(authorized_user)
        except:
            config.log.exception('MAIN_ERROR')


if __name__ == '__main__':
    main()
