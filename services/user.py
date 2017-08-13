import recaptcha2
from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home

from app import app, db
from models.user import User
from services.flasksqlalchemy import FlaskSQLAlchemy
from services.flasklogging import FlaskLogging

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
            new_user.title = user['title']
            if user['description']:
                new_user.description = user['description']

            return flask_sql_alchemy.add(new_user)
        else:
            errors.append('Failed to register. Email already exists')
            return {'success': False, 'errors': errors}

    def get_user(self, user_id):
        user = {}
        try:
            result = User\
                .query\
                .with_entities(User.id.label('id'), User.first_name.label('first_name'),
                               User.last_name.label('last_name'), User.email.label('email'),
                               User.gender.label('gender'), User.zipcode.label('zipcode'))\
                .filter(User.id == user_id)
            if not result[0].gender:
                image_url = 'https://i.stack.imgur.com/IHLNO.jpg'
            else:
                image_url = 'https://randomuser.me/api/portraits/'
                if result[0].gender == 'm':
                    image_url += 'men/'
                else:
                    image_url += 'women/'

                # use 50 images, then recycle
                image_num = int(user_id) % 50
                if image_num == 0:
                    image_num = 1
                image_url += str(image_num) + '.jpg'

            user = {"id": user_id, "first_name": result[0].first_name, "last_name": result[0].last_name,
                    "email": result[0].email, "gender": result[0].gender, "zipcode": result[0].zipcode,
                    "image": image_url}
        except Exception as e:
            flask_logging = FlaskLogging()
            flask_logging.log_info(str(e))
        return user
