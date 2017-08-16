# https://www.youtube.com/watch?v=_5OXmXvkU_E

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'some_secret'
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from routes import *

if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)

