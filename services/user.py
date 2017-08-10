import recaptcha2
from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home

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
        errors = []

        if len(user['first_name']) == 0:
            errors.append('First name cannot be empty')
        if len(user['last_name']) == 0:
            errors.append('Last name cannot be empty')
        if len(user['email']) == 0:
            errors.append('Email cannot be empty')
        if len(user['password']) == 0:
            errors.append('Password cannot be empty')
        if len(user['confirm_password']) == 0:
            errors.append('Confirm password cannot be empty')
        if user['password'] != user['confirm_password']:
            errors.append('Password and Confirm password should match')
        if len(user['recaptcha']) == 0:
            errors.append('Recaptcha cannot be empty')
        if len(user['gender']) == 0:
            errors.append('Must select a gender')
        if len(user['zipcode']) == 0:
            errors.append('Zipcode cannot be empty')
        if len(user['zipcode']) != 5:
            errors.append('Zipcode must be 5 digit long')
        if not user['zipcode'].isnumeric():
            errors.append('Zipcode must be a valid 5 digit number')

        if errors:
            return {'success': False, 'errors': errors}

        password_hash = pwd_context.hash(user['password'])
        flask_sql_alchemy = FlaskSQLAlchemy()
        count = flask_sql_alchemy.count('User', {'val1': User.email, 'val2': user['email'], 'operation': 'eq'})
        if not count:
            new_user = User()
            new_user.email = user['email']
            new_user.first_name = user['first_name']
            new_user.last_name = user['last_name']
            new_user.password = password_hash
            new_user.gender = user['gender']
            new_user.zipcode = user['zipcode']

            return flask_sql_alchemy.add(new_user)
        else:
            errors.append('Failed to register. Email already exists')
            return {'success': False, 'errors': errors}



