from flask import render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import text
from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home

from app import app, db
from services.user import UserService
from services.auth import AuthService

login_manager = LoginManager()
login_manager.init_app(app)


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


@login_manager.user_loader
def load_user(user_id):
    user_service = UserService()
    user = user_service.load_user(user_id)
    return user

@app.route('/flask-login-login/<user_id>')
def flask_login_login(user_id):
    user_service = UserService()
    user = user_service.load_user(user_id)
    login_user(user)
    return "You are now logged in"

@app.route('/flask-login-logout')
@login_required
def flask_login_logout():
    logout_user()
    return "You are now logged out"


@app.route('/flask-login-home')
@login_required
def flask_login_home():
    return "The current user is " + current_user.first_name + " " + current_user.last_name


@app.route('/update-account', methods=['POST'])
def update_account():
    if request.method == 'POST':
        user_data = {
            'user_id': request.form['user_id'],
            'first_name': request.form['firstName'],
            'last_name': request.form['lastName'],
            'gender': request.form['gender'],
            'zipcode': request.form['zipcode'],
            'title': request.form['title']
        }
        user_service = UserService()
        update_account_result = user_service.update_user_account(user_data)
        if update_account_result['success']:
            flash('Successfully updated user account', 'success')
        else:
            # try flask flash
            flash('There was an error in updating your information', 'danger')
        return redirect(url_for('.get_user', user_id=request.form['user_id']))


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/post-json', methods=['POST'])
def post_json():
    json_dict = request.get_json()
    input_text = json_dict['input_text']
    data = {'output_text': input_text + ' came back from server at ' + str(datetime.now())}
    return jsonify(data)