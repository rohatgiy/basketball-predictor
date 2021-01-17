from flask import Flask, redirect, url_for, request, render_template
import tensorflow as tf
from tensorflow import keras
from test import getResults
from model import setup
#from wtforms import Form, BooleanField, StringField, validators, SelectField


app = Flask(__name__)
teamnames = []
with open("teamnames.txt") as fileIn:
    for line in fileIn:
        teamnames.append(line.strip().split("\n")[0])

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/predict', methods=["GET"])
def predict():
    return render_template("predict.html", teams=teamnames)

@app.route('/results', methods=["POST"])
def results():
    homeIndex = int(request.form["homeTeam"])
    awayIndex = int(request.form["awayTeam"])
    homeWin = (getResults(awayIndex, homeIndex))
    homeWin = round(homeWin*100, 2)
    homeTeamName = teamnames[homeIndex]
    awayTeamName = teamnames[awayIndex]
    return render_template("results.html", home_win = homeWin, home_lose = round(100 - homeWin, 2), home_team_name = homeTeamName, away_team_name = awayTeamName)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.errorhandler(405)
def unauthorized_method(e):
    return redirect(url_for('index'))
