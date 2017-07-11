from app import db
from services.flasklogging import FlaskLogging

class FlaskSQLAlchemy:

    def __init__(self):
        self.db = db.session
        self.filter_val = ''
        self.flask_logging = FlaskLogging()

    def add(self, obj):
        try:
            self.db.add(obj)
            if self.commit():
                # todo: get new user information from flask_user and flask_role tables
                return {'success': True}
        except Exception as e:
            return self.error_message(e)

    def commit(self):
        try:
            self.db.commit()
            return {'success': True}
        except Exception as e:
            return self.error_message(e)

    def query(self, model):
        try:
            return self.db.query(model)
        except Exception as e:
            return self.error_message(e)

    def filter(self, val1=None, val2=None, operation='eq'):
        try:
            # return self.db.filter(val1 + operation + val2)

            self.filter_val = ''
            if val1 and val2:
                self.filter_val = val1 + operation + val2
        except Exception as e:
            return self.error_message(e)

    def count(self, model, filter_values=None):
        try:
            val1 = filter_values['val1']
            val2 = filter_values['val2']
            operation = filter_values['operation']

            if filter_values:
                #count_result = self.db.query(model).filter(self.filter(val1, val2, operation)).count()
                count_result = self.db.query(model).filter(val1 == val2).count()
            else:
                count_result = self.db.query(model).filter(self.filter()).count()

            return count_result
            #return self.db.count()
        except Exception as e:
            return self.error_message(e)

    @staticmethod
    def error_message(self, error_message=None):
        if not error_message:
            error_message = 'Something went wrong'
            self.flask_logging.log_error(error_message)
        return {'success': False, 'error_message': error_message}