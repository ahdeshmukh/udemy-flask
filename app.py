from flask import Flask, render_template, request, jsonify
from datetime import datetime
import psycopg2, psycopg2.extras, sys

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/show-users')
def show_users():
    users = [
        {"first_name": "Roy", "last_name": "Swanson"},
        {"first_name": "Heather", "last_name": "Lee"},
        {"first_name": "Curtis", "last_name": "Wallace"},
        {"first_name": "Jessica", "last_name": "Lopez"},
    ]
    db_con = None
    try:
        db_con = psycopg2.connect(host='localhost', database='flask_db', user='amit', password='password')
        cursor = db_con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT id, first_name, last_name, email FROM users")
        users = cursor.fetchall()
    except psycopg2.DatabaseError as e:
        print(e)
        sys.exit(1)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    finally:
        if db_con is not None:
            db_con.close()

    print('coming here')
    return render_template('users.html', users=users)


@app.route('/post-json', methods=["POST"])
def post_json():
    json_dict = request.get_json()
    input_text = json_dict['input_text']
    data = {'output_text': input_text + ' came back from server at ' + str(datetime.now())}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)