from flask import Flask, render_template, request, jsonify

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
    content = request.json
    print(content['mytext'])

if __name__ == "__main__":
    app.run(debug=True)