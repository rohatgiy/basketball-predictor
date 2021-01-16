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

URLs = ["http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2015/league/00_full_schedule.json", "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2016/league/00_full_schedule.json",
"http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/league/00_full_schedule.json", "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2018/league/00_full_schedule.json", 
"http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json", "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json"]
allPlayers = []
pogPlayers = []
pogVorpPlayers = []
playerTeamDict = {}
playerStatsDict = {}
dataset = []

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
            print(player)
            pogVorpPlayers.append(player)
        playerStatsDict[player] = [vorp, gp, health]

for team in teamAbbrvs:
    pogPlayers.append({})

model = keras.Sequential()

model.add(keras.layers.Dense(256,input_shape=(6,), activation="relu"))
model.add(keras.layers.Dense(875, input_shape=(256,), activation="relu"))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(1, activation="sigmoid"))

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    
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
                    gameData.append(int(currentGame["v"]["s"]))
                    gameData.append(int(currentGame["h"]["s"]))
                    dataset.append(gameData)
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
                        #print(pogPlayers)
    
    #for team in pogPlayers:
    #    for player in team.keys():
    #        if team[player] < 

'''
def filterPogPlayers():
    for team in pogPlayers:
        for player in team.items():
            if player in playerStatsDict:
'''

def main():
    for url in URLs:
        gatherStats(url)
    with open("dataset.json", "w") as fileOut:
        json.dump(dataset, fileOut)
        fileOut.write('\n')
    #print(pogPlayers)
    filteredPogPlayers = []
    for team in pogPlayers:
        newEntry = dict(filter(lambda elem: (elem[0] in playerStatsDict) and (elem[0] in pogVorpPlayers) and (playerStatsDict[elem[0]][2] == "Healthy") and (playerStatsDict[elem[0]][1] > 100) and (elem[1] / playerStatsDict[elem[0]][1] > 0.1), team.items()))
        print(newEntry)
        filteredPogPlayers.append(newEntry)
    #print(filteredPogPlayers)
    #print(pogVorpPlayers)
    #print(playerStatsDict)

if __name__ == "__main__":
    main()

    #get_odds("LAL", "NOP")
    #print(pogPlayers)
    #main()
