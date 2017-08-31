from services.flasklogging import FlaskLogging

class FlaskError:

    def __init__(self):
        self.flask_logging = FlaskLogging()

    def error_message(self, error_message=None, is_exception=False):
        if not error_message:
            error_message = 'Something went wrong'
            self.flask_logging.log_error(error_message)
        return {'success': False, 'error_message': error_message, 'is_exception': is_exception}