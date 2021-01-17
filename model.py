import tensorflow as tf
import numpy as np
from tensorflow import keras
import requests
import json

# "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json"
# http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json

# if obj["lscd"][month]["mscd"]["g"][game]["stt"] == "Final":
#   print(f'visitor: {obj["lscd"][month]["mscd"]["g"][game]["v"]["ta"]}\nhome: {obj["lscd"][month]["mscd"]["g"][game]["h"]["ta"]}')

teamAbbrvs = ["ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", 
"LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]

teamScores=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

URLs = ["http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2015/league/00_full_schedule.json", "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2016/league/00_full_schedule.json",
"http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/league/00_full_schedule.json", "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2018/league/00_full_schedule.json", 
"http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json", "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json"]
allPlayers = []
pogPlayers = []
pogVorpPlayers = []
playerTeamDict = {}
playerStatsDict = {}
data = []
filteredPogPlayers = []
ans = []
model = keras.Sequential()

with open("roster.txt") as fileIn:
    for line in fileIn:
        player = line.strip().split("%")[0]
        team = int(line.strip().split("%")[1])
        allPlayers.append(player)
        playerTeamDict[player] = team

with open("stats.txt") as fileIn:
    for line in fileIn:
        player = line.strip().split("%")[0]
        vorp = float(line.strip().split("%")[1])
        gp = int(line.strip().split("%")[2])
        health = line.strip().split("%")[3]
        if type(vorp) == float and vorp >= 1.5:
            #print(player)
            pogVorpPlayers.append(player)
        playerStatsDict[player] = [vorp, gp, health]

for team in teamAbbrvs:
    pogPlayers.append({})

def get_odds(team1, team2):
    return model.predict([team1, team2, teamScores[team1], teamScores[team2], len(filteredPogPlayers[team1]), len(filteredPogPlayers[team2])])

def gatherStats(url):
    res = requests.get(url)
    obj = res.json()
    for month in range(len(obj["lscd"])):
        gameList = obj["lscd"][month]["mscd"]["g"]
        for game in range(len(gameList)):
            gameData = []
            currentGame = gameList[game]
            if currentGame["stt"] == "Final":
                if currentGame["v"]["ta"] in teamAbbrvs and currentGame["h"]["ta"] in teamAbbrvs:
                    gameData.append(teamAbbrvs.index(currentGame["v"]["ta"]))
                    gameData.append(teamAbbrvs.index(currentGame["h"]["ta"]))
                    gameData.append(float(currentGame["v"]["s"]))
                    gameData.append(float(currentGame["h"]["s"]))

                    ans.append(float(1) if float(currentGame["h"]["s"]) > float(currentGame["v"]["s"]) else float(0))

                    teamScores[teamAbbrvs.index(currentGame["v"]["ta"])] += float(currentGame["v"]["s"])
                    teamScores[teamAbbrvs.index(currentGame["h"]["ta"])] += float(currentGame["h"]["s"])

                    data.append(gameData)
                highScorers = currentGame["ptsls"]["pl"]
                for player in highScorers:
                    playerFullName = player["fn"] + ' ' + player["ln"]
                    #print(player["ta"])
                    if player["ta"] in teamAbbrvs and playerFullName in allPlayers:
                        playerTeamIndex = playerTeamDict[playerFullName]

                        if playerFullName not in pogPlayers[playerTeamIndex]:
                            pogPlayers[playerTeamIndex][playerFullName] = 1
                        else :
                            pogPlayers[playerTeamIndex][playerFullName] += 1

def add_players():
    for gdata in data:
        gdata.append(len(filteredPogPlayers[gdata[0]]))
        gdata.append(len(filteredPogPlayers[gdata[0]]))    

def main():

    model.add(keras.layers.Dense(256,input_shape=(6,), activation="relu"))
    #model.add(keras.layers.Dense(875, input_shape=(256,), activation="relu"))
    #model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(1, activation="sigmoid"))

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    for url in URLs:
        gatherStats(url)
    for team in pogPlayers:
        newEntry = dict(filter(lambda elem: (elem[0] in playerStatsDict) and (elem[0] in pogVorpPlayers) and (playerStatsDict[elem[0]][2] == "Healthy") and (playerStatsDict[elem[0]][1] > 100) and (elem[1] / playerStatsDict[elem[0]][1] > 0.1), team.items()))
        filteredPogPlayers.append(newEntry)
    add_players()
    model.fit(data, ans, epochs=50)
    print(get_odds(0, 9))

if __name__ == "__main__":
    main()