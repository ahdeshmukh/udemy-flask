from app import app


class FlaskLogging:

    def __init__(self):
        self.app = app

    def log_warning(self, msg, args=None, kwargs=None):
        self.app.logger.warning(msg, args, kwargs)

    def log_info(self, msg, args=None, kwargs=None):
        self.app.logger.info(msg, args, kwargs)

    def log_error(self, msg, args=None, kwargs=None):
        self.app.logger.error(msg, args, kwargs)