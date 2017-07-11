from flask import render_template, request, jsonify
from datetime import datetime
from sqlalchemy import text
import recaptcha2
from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home

from app import app, db
from models.user import User
from services.user import UserService


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register-success', methods=["POST"])
def register_success():
    if request.method == 'POST':
        registration_data = {
            'email': request.form['email'],
            'first_name': request.form['firstName'],
            'last_name': request.form['lastName'],
            'password': request.form['password'],
            'confirm_password': request.form['confirmPassword'],
            'recaptcha': request.form['g-recaptcha-response'],
            'gender': request.form['gender']
        }

        user_service = UserService()
        user_registration_result = user_service.register(registration_data)
        if user_registration_result['success']:
            return "Registered successfully"
        else:
            return "Error in registering the user"


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