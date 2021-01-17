from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return "this is index"

@app.route('/predict', methods=["GET"])
def predict():
    return "predict here"

@app.route('/results', methods=["POST"])
def results():
    return request.form

@app.errorhandler(404, 405)
def page_not_found(e):
    return redirect(url_for('index'))
