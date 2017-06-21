from flask import Flask, render_template, request, jsonify
from datetime import datetime
import psycopg2, psycopg2.extras, sys

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/success', methods=["POST"])
def success():
    return render_template("success.html")


@app.route('/post-json', methods=["POST"])
def post_json():
    json_dict = request.get_json()
    input_text = json_dict['input_text']
    data = {'output_text': input_text + ' came back from server at ' + str(datetime.now())}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)