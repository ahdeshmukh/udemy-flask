import recaptcha2
from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home
from pprint import pprint

from app import app, db
from models.user import User
from services.flasksqlalchemy import FlaskSQLAlchemy

class UserService:

    def register(self, user):
        registration_error = []
        if len(user['recaptcha']) == 0:
            registration_error.append('Recaptcha cannot be empty')
        else:
            # validating user recaptcha input
            recaptcha_validation_response = recaptcha2.verify(app.config['GOOGLE_RECAPTCHA_SECRET'], user['recaptcha'])
            if recaptcha_validation_response is None or recaptcha_validation_response['success'] is None or recaptcha_validation_response['success'] is False:
                registration_error.append('Recaptcha cannot be verified')

        if registration_error:
            return {'success': False, 'errors': registration_error}

        return self.add_user(user)

    def add_user(self, user):
        error_messages = []

        if len(user['first_name']) == 0:
            error_messages.append('First name cannot be empty')
        if len(user['last_name']) == 0:
            error_messages.append('Last name cannot be empty')
        if len(user['email']) == 0:
            error_messages.append('Email cannot be empty')
        if len(user['password']) == 0:
            error_messages.append('Password cannot be empty')
        if len(user['confirm_password']) == 0:
            error_messages.append('Confirm password cannot be empty')

        #user.recaptcha = 'abc'
        if len(user['recaptcha']) == 0:
            error_messages.append('Recaptcha cannot be empty')
        if user['password'] != user['confirm_password']:
            error_messages.append('Password and Confirm password should match')
        if len(user['gender']) == 0:
            error_messages.append('Must select a gender')

        if error_messages:
            return {'success': False, 'error_messages': error_messages}

        password_hash = pwd_context.hash(user['password'])
        #if not db.session.query(User).filter(User.email == user.email).count():
        flasksqlalchemy = FlaskSQLAlchemy()

        #query = flasksqlalchemy.query(User)
        #filter = flasksqlalchemy.filter(User.email, user['email'], '==')
        count = flasksqlalchemy.count('User', {'val1': User.email, 'val2': user['email'], 'operation': 'eq'})
        if not count:
            new_user = User(user['email'], user['first_name'], user['last_name'], password_hash, user['gender'])
            #db.session.add(new_user)
            #db.session.commit()
            new_user_result = flasksqlalchemy.add(new_user)
            app.logger.error(new_user_result)
            return new_user_result
        else:
            return {'success': False, 'error_messages': 'Failed to register. Email already exists.'}



