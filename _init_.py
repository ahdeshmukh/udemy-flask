from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<userxyz>')
def hello_name(userxyz):
    return render_template('user.html', nameabc=userxyz)


@app.route('/post-json', methods=["POST"])
def post_json():
    json_dict = request.get_json()
    input_text = json_dict['input_text']
    data = {'output_text': input_text + ' came back from server at ' + str(datetime.now())}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)