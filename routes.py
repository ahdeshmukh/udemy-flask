from flask import render_template, request, jsonify, redirect, url_for, flash, g
from datetime import datetime
from flask_login import LoginManager, login_required

from app import app, db
from services.user import UserService
from services.auth import AuthService

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    user_service = UserService()
    current_user = user_service.get_current_user()
    try:
        if current_user:
            return redirect(url_for('.get_user', user_id=current_user.id))
    except:
        pass
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    user_service = UserService()
    current_user = user_service.get_current_user()
    try:
        if current_user:
            return redirect(url_for('.get_user', user_id=current_user.id))
    except:
        pass

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
            user = login_result['user']
            #login_user(user, remember=True) #https://flask-login.readthedocs.io/en/latest/#remember-me
            user_service = UserService()
            user_service.login_user(user)
            g.user = user
            return redirect(url_for('.get_user', user_id=user.id))

    return render_template("login.html", invalid_credentials=True)


@app.route('/logout')
@login_required
def logout():
    user_service = UserService()
    if user_service.logout_user():
        flash('Successfully logged out', 'success')
    else:
        # try flask flash
        flash('Error in logging you out. Please try again later', 'danger')
    return redirect(url_for('.index'))


@app.route('/user/<user_id>')
@login_required
def get_user(user_id):
    user_service = UserService()
    user = user_service.get_current_user()
    #user = current_user
    return render_template("profile.html", user=user)


@app.route('/users')
@login_required
def get_users():
    user_service = UserService()
    users = user_service.get_users()
    user = user_service.get_current_user()
    return render_template("users.html", users=users)

@login_manager.user_loader
def load_user(user_id):
    user_service = UserService()
    user = user_service.load_user(user_id)
    return user


@app.route('/update-account', methods=['POST'])
@login_required
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
    user_service = UserService()
    user = user_service.get_current_user()
    if hasattr(user, 'id'):
        return render_template("about.html", user=user)
    return render_template("about.html")

# common variables to be used across all templates. http://flask.pocoo.org/docs/0.12/templating/
@app.context_processor
def header_processor():
    user_service = UserService()
    user = user_service.get_current_user()
    is_admin = user_service.is_admin()
    return dict(user=user, is_admin=is_admin)


@app.route('/post-json', methods=['POST'])
def post_json():
    json_dict = request.get_json()
    input_text = json_dict['input_text']
    data = {'output_text': input_text + ' came back from server at ' + str(datetime.now())}
    return jsonify(data)