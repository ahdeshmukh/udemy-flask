import sys, os
from app import db
from services.flaskerror import FlaskError
from models.exception import FlaskException


class FlaskSQLAlchemy():

    def __init__(self):
        self.db = db.session
        self.filter_val = ''
        self.flask_error = FlaskError()

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

    def filter(self, model, model_val, actual_val, limit=None, operation='eq'):
        try:
            return self.db.query(model).filter(getattr(model, model_val) == actual_val)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(fname, exc_tb.tb_lineno)
            exception = FlaskException()
            exception.error = str(e)
            exception.message = 'Error in database query'
            self.flask_sql_alchemy.add(exception)
            return self.error_message(e, True)

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

    def error_message(self, error_message=None):
        return self.flask_error.error_message(error_message)