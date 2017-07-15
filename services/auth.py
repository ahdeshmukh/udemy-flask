from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home
from sqlalchemy import text

from app import app, db


class AuthService:

    def login(self, credentials):
        login_error = []
        if len(credentials['email']) == 0:
            login_error.append('Email cannot be empty')
        if len(credentials['password']) == 0:
            login_error.append('Password cannot be empty')

        if login_error:
            return {'success': False, 'errors': login_error}

        sql = text('SELECT id, first_name, last_name, email, password, zipcode FROM flask_user WHERE email = :email')
        result = db.engine.execute(sql, email=credentials['email'])

        auth = False
        for row in result:
            auth = pwd_context.verify(credentials['password'], row['password'])

        if auth:
            user = {'first_name': row['first_name'], 'last_name': row['last_name'], 'email': row['email'],
                    'zipcode': row['zipcode']}
            return {'success': True, 'user': user}

        login_error.append('Invalid Usernamexxx or password')
        return {'success': False, 'errors': login_error}

