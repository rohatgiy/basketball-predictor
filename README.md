## ProbaBall

![logo](/static/probaball_logo.png/)

## Table of Contents
- [Introduction](#introduction)
- [Data and Technologies](#data-and-technologies)
- [Screenshots](#screenshots)

## Introduction
ProbaBall was created by first-years Yash Rohatgi and Kevin Lee as their submission to Hack The Northeast 2021.
It serves to predict the outcome of an NBA match between any two given teams using a trained Machine Learning model.
It was developed from the ground-up within the span of 36 hours with use of the Python library TensorFlow, the micro-framework
Flask, and front-end technologies such as HTML, CSS and JavaScript Bootstrap.


## Data and Technologies
The data that was used to train the model can be found in the following links:
[2015-2016 NBA Season Data](#http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2015/league/00_full_schedule.json)
[2016-2017 NBA Season Data](#http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2016/league/00_full_schedule.json)
[2017-2018 NBA Season Data](#http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/league/00_full_schedule.json)
[2018-2019 NBA Season Data](#http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2018/league/00_full_schedule.json)
[2019-2020 NBA Season Data](#http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json)
[2020-2021 NBA Season Data](#http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json)
[2020-2021 NBA Roster Data](#https://raw.githubusercontent.com/alexnoob/BasketBall-GM-Rosters/master/2020-21.NBA.Roster.json)

The datasets above contain game data from the past six NBA seasons (including preseason and playoffs) from each team, amounting to around
15,000 entries. The last dataset contains complete statistics of every registered NBA player since the start of their career up until
the file's last update (January 14, 2021, or 5 days ago, at the time of writing this README).

Using Python File I/O, the data was parsed and statistics such as Offensive Rating, Defensive Rating, Previous Season and Playoff Record,
Current Record, Player VORPs and top scoring players in each game were all extracted into their respective data structures as numerical values.
Once the data structures were built, we trained our model with TensorFlow to determine how to weigh each factor in terms of helping a team win, using around 
13,000 of all the entries.

Once the trained model was saved, it was loaded and incorporated into an HTML web page using Flask, allowing the user to provide input from HTML
which could then be used in an imported Python function using the saved model.

Formatting and design was then completed using JavaScript, CSS, and Bootstrap.


## Screenshots
![Homepage](/static/indexss.png/)
![Predictpage](/static/predictss.png/)
![Resultpage](/static/resultsss.png/)
