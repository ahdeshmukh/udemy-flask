from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home
from sqlalchemy import text
from datetime import datetime

from app import app, db
from services.user import UserService

class AuthService:

    def login(self, credentials):
        login_error = []
        if len(credentials['email']) == 0:
            login_error.append('Email cannot be empty')
        if len(credentials['password']) == 0:
            login_error.append('Password cannot be empty')

        if login_error:
            return {'success': False, 'errors': login_error}

        user_service = UserService()
        user = user_service.load_user_by_email(credentials['email'])

        auth = False
        if user:
            try:
                auth = pwd_context.verify(credentials['password'], user.password)
            except:
                pass

            if auth:
                update_last_login_sql = text('UPDATE flask_user SET last_login = :last_login WHERE id = :id')
                db.engine.execute(update_last_login_sql, last_login=str(datetime.now()), id=user.id)
                return {'success': True, 'user': user}

        login_error.append('Invalid Username or password')
        return {'success': False, 'errors': login_error}

