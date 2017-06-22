from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://amit:password@localhost/flask_db'
app.config['GOOGLE_RECAPTCHA_SECRET'] = '6LfKcCYUAAAAAJXHWL48hMFZxTcD4Ruv3ANi8Rzb'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email, height):
        self.email = email
        self.height = height


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register-success', methods=["POST"])
def register_success():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        recaptcha = request.form['g-recaptcha-response']
        print(first_name)
        print(email)
        print(recaptcha)
        return "Registered successfully"


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