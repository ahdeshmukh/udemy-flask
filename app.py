from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import recaptcha2
from passlib.apps import custom_app_context as pwd_context #https://bitbucket.org/ecollins/passlib/wiki/Home

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "flask_user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(255))
    gender = db.Column(db.String(1))

    def __init__(self, email, first_name, last_name, password, gender):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.gender = gender


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register-success', methods=["POST"])
def register_success():
    if request.method == 'POST':
        email = request.form['email'].strip()
        first_name = request.form['firstName'].strip()
        last_name = request.form['lastName'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirmPassword'].strip()
        recaptcha = request.form['g-recaptcha-response']
        gender = request.form['gender']

        if len(first_name) == 0:
            print('First name cannot be empty')
        if len(last_name) == 0:
            print('Last name cannot be empty')
        if len(email) == 0:
            print('Email cannot be empty')
        if len(password) == 0:
            print('Password cannot be empty')
        if len(confirm_password) == 0:
            print('Confirm password cannot be empty')
        if len(recaptcha) == 0:
            print('Recaptcha cannot be empty')
        if password != confirm_password:
            print('Password and Confirm password should match')
        if len(gender) == 0:
            print('Must select a gender')

        # validating user recaptcha input
        resp = recaptcha2.verify(app.config['GOOGLE_RECAPTCHA_SECRET'], recaptcha)
        if resp is None or resp['success'] is None or resp['success'] is False:
            # Todo: show error saying recaptcha cannot be verified"""
            pass

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


@app.route('/success', methods=["POST"])
def success():
    if request.method == 'POST':
        email = request.form['email_name']
        height = request.form['height_name']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            user = User(email, height)
            db.session.add(user)
            db.session.commit()
            return render_template("success.html")

        return render_template("index.html", message="Email "+ email + " already exists")


@app.route('/post-json', methods=["POST"])
def post_json():
    json_dict = request.get_json()
    input_text = json_dict['input_text']
    data = {'output_text': input_text + ' came back from server at ' + str(datetime.now())}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)