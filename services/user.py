import recaptcha2
from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home
from validate_email import validate_email #https://pypi.python.org/pypi/validate_email
from flask_login import current_user, login_user, logout_user
from sqlalchemy import text

from app import app, db
from models.user import User
from services.flasksqlalchemy import FlaskSQLAlchemy
from services.flasklogging import FlaskLogging

class UserService:
    flask_sql_alchemy = FlaskSQLAlchemy()
    flask_logging = FlaskLogging()

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
        if not validate_email(user['email']):
            errors.append('Invalid email format. Eg: of valid format: john.doe@example.com')
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
        if len(user['title']) == 0:
            errors.append('Title cannot be empty')
        if len(user['zipcode']) == 0:
            errors.append('Zipcode cannot be empty')
        if len(user['zipcode']) != 5:
            errors.append('Zipcode must be 5 digit long')
        if not user['zipcode'].isnumeric():
            errors.append('Zipcode must be a valid 5 digit number')

        if errors:
            return {'success': False, 'errors': errors}

        password_hash = pwd_context.hash(user['password'])
        #flask_sql_alchemy = FlaskSQLAlchemy()
        count = self.flask_sql_alchemy.count('User', {'val1': User.email, 'val2': user['email'], 'operation': 'eq'})
        if not count:
            new_user = User()
            new_user.email = user['email']
            new_user.first_name = user['first_name']
            new_user.last_name = user['last_name']
            new_user.password = password_hash
            new_user.gender = user['gender']
            new_user.zipcode = user['zipcode']
            new_user.title = user['title']
            if 'description' in user:
                new_user.description = user['description']

            return self.flask_sql_alchemy.add(new_user)
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
                               User.gender.label('gender'), User.zipcode.label('zipcode'),
                               User.title.label('title'))\
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
                    "title": result[0].title, "image": image_url}
        except Exception as e:
            self.flask_logging.log_info(str(e))
        return user

    def update_user_account(self, user_data):
        errors = []

        if len(user_data['first_name']) == 0:
            errors.append('First name cannot be empty')
        if len(user_data['last_name']) == 0:
            errors.append('Last name cannot be empty')
        if len(user_data['title']) == 0:
            errors.append('Title cannot be empty')
        if len(user_data['zipcode']) == 0:
            errors.append('Zipcode cannot be empty')
        if len(user_data['zipcode']) != 5:
            errors.append('Zipcode must be 5 digit long')
        if not user_data['zipcode'].isnumeric():
            errors.append('Zipcode must be a valid 5 digit number')
        if not self.is_admin() and len(user_data['gender']) == 0:
            errors.append('Must select a gender')

        if errors:
            return {'success': False, 'errors': errors}

        user = User.query.filter_by(id=user_data['user_id']).first()
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.zipcode = user_data['zipcode']
        user.title = user_data['title']
        if not self.is_admin():
            user.gender = user_data['gender']
            user.gender = user_data['gender']

        # TODO: FlaskSQLAlchemy as a strategy pattern
        return self.flask_sql_alchemy.commit()

    def load_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None

        user.image = self.get_user_image(user)
        user.roles = [1] # all users have authenticated role
        roles_query = text('SELECT role_id FROM flask_user_role WHERE user_id = :user_id')
        roles_result = db.engine.execute(roles_query, user_id=user_id)
        for role in roles_result:
            user.roles.extend(role)
        return user

    def get_current_user(self):
        return current_user

    def get_user_image(self, user):
        image_url = 'https://i.stack.imgur.com/IHLNO.jpg'
        if user.gender:
            image_url = 'https://randomuser.me/api/portraits/'
            if user.gender == 'm':
                image_url += 'men/'
            else:
                image_url += 'women/'

            image_num = int(user.id) % 50
            if image_num == 0:
                image_num = 1
            image_url += str(image_num) + '.jpg'

        return image_url

    def load_user_by_email(self, email):
        #TODO: get id from flask_user table based on email and then use load_user function
        user = None
        result = User.query.filter(User.email == email).limit(1)
        try:
            user = result[0]
            user.image = self.get_user_image(user)
            user.roles = [1]  # all users have authenticated role
            roles_query = text('SELECT role_id FROM flask_user_role WHERE user_id = :user_id')
            roles_result = db.engine.execute(roles_query, user_id=user.id)
            for role in roles_result:
                user.roles.extend(role)
        except:
            pass
        return user

    def login_user(self, user, remember=True):
        login_user(user, remember=remember) #https://flask-login.readthedocs.io/en/latest/#remember-me

    def logout_user(self):
        return logout_user()

    def is_admin(self):
        user = self.get_current_user()
        is_admin = False
        try:
            if 2 in user.roles:
                is_admin = True
        except:
            pass

        return is_admin

    def get_users(self):
        data = []
        if self.is_admin():
            users = User.query.all()
            for user in users:
                image = self.get_user_image(user)
                if user.id != 1:
                    data.append({"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "image": image})

        return data
