from models.exception import FlaskException
from services.flasksqlalchemy import FlaskSQLAlchemy


class FlaskExceptionService:
    def __init__(self, message, error):
        self.flask_sql_alchemy = FlaskSQLAlchemy()
        self.message = message
        self.error = error

    def log_exception(self):
        flask_exception = FlaskException()
        flask_exception.message = self.message
        flask_exception.error = self.error
        return self.flask_sql_alchemy.add(flask_exception)
