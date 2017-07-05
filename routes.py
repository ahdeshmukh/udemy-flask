from flask import render_template, request, jsonify
from datetime import datetime
from sqlalchemy import text
import recaptcha2
from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home

from app import app, db
from models.user import User


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register-success', methods=["POST"])
def register_success():
    error_messages = []
    if request.method == 'POST':
        email = request.form['email'].strip()
        first_name = request.form['firstName'].strip()
        last_name = request.form['lastName'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirmPassword'].strip()
        recaptcha = request.form['g-recaptcha-response']
        gender = request.form['gender']

        if len(first_name) == 0:
            error_messages.append('First name cannot be empty')
        if len(last_name) == 0:
            error_messages.append('Last name cannot be empty')
        if len(email) == 0:
            error_messages.append('Email cannot be empty')
        if len(password) == 0:
            error_messages.append('Password cannot be empty')
        if len(confirm_password) == 0:
            error_messages.append('Confirm password cannot be empty')
        if len(recaptcha) == 0:
            error_messages.append('Recaptcha cannot be empty')
        if password != confirm_password:
            error_messages.append('Password and Confirm password should match')
        if len(gender) == 0:
            error_messages.append('Must select a gender')

        # validating user recaptcha input
        recaptcha_validation_response = recaptcha2.verify(app.config['GOOGLE_RECAPTCHA_SECRET'], recaptcha)
        if recaptcha_validation_response is None or recaptcha_validation_response['success'] is None or recaptcha_validation_response['success'] is False:
            # Todo: show error saying recaptcha cannot be verified"""
            error_messages.append('Recaptcha cannot be verified')

        if error_messages:
            return render_template("register.html", errorMessages=error_messages)

        password_hash = pwd_context.hash(password)
        if not db.session.query(User).filter(User.email == email).count():
            user = User(email, first_name, last_name, password_hash, gender)
            db.session.add(user)
            db.session.commit()
        return "Registered successfully"


@app.route('/login', methods=["POST"])
def login_success():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql = text('select id, first_name, last_name, email, password from flask_user where email = :email')
        result = db.engine.execute(sql, email=email)
        auth = False
        first_name = ''
        last_name = ''
        for row in result:
            auth = pwd_context.verify(password, row['password'])
            first_name = row['first_name']
            last_name = row['last_name']

        if auth:
            user = {'first_name':first_name, 'last_name':last_name}
            return render_template("profile.html", user=user)

    return render_template("login.html", invalidCredentials=True)


@app.route('/post-json', methods=["POST"])
def post_json():
    json_dict = request.get_json()
    input_text = json_dict['input_text']
    data = {'output_text': input_text + ' came back from server at ' + str(datetime.now())}
    return jsonify(data)