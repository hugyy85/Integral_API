import auth
import db.operations
import main_menu
import config


def main():
    db.operations.create_database()
    db.operations.create_tables()
    while True:
        try:
            # authorization and registration
            authorized_user = auth.auth()
            # menu registered users
            main_menu.main(authorized_user)
        except:
            config.log.exception('MAIN_ERROR')


if __name__ == '__main__':
    main()
