from flask import render_template, request, jsonify, redirect,url_for
from datetime import datetime
from sqlalchemy import text
from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home

from app import app, db
from services.user import UserService
from services.auth import AuthService


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_errors = None
    if request.method == 'POST':
        registration_data = {
            'email': request.form['email'],
            'first_name': request.form['firstName'],
            'last_name': request.form['lastName'],
            'password': request.form['password'],
            'confirm_password': request.form['confirmPassword'],
            'recaptcha': request.form['g-recaptcha-response'],
            'gender': request.form['gender'],
            'zipcode': request.form['zipcode'],
            'title': request.form['title']
        }

        user_service = UserService()
        user_registration_result = user_service.register(registration_data)
        if user_registration_result['success']:
            return render_template('login.html', register_success=True)
        else:
            registration_errors = ['Error in registering the user']
            if user_registration_result['errors']:
                registration_errors = user_registration_result['errors']

    return render_template('register.html', registration_errors=registration_errors)


@app.route('/login', methods=['POST'])
def login_success():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth_service = AuthService()
        login_result = auth_service.login({'email': email, 'password': password})

        if login_result['success']:
            #return render_template("profile.html", user=login_result['user'])
            # return redirect(url_for("get_user", user=login_result['user']))
            return redirect(url_for('.get_user', user_id=login_result['user']['id']))

    return render_template("login.html", invalid_credentials=True)


@app.route('/user/<user_id>')
def get_user(user_id):
    user_service = UserService()
    user = user_service.get_user(user_id)
    return render_template("profile.html", user=user)


@app.route('/post-json', methods=['POST'])
def post_json():
    json_dict = request.get_json()
    input_text = json_dict['input_text']
    data = {'output_text': input_text + ' came back from server at ' + str(datetime.now())}
    return jsonify(data)