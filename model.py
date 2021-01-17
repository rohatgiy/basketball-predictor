import tensorflow as tf
import numpy as np
from tensorflow import keras
import requests
import json
import time

# "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json"
# http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json

# if obj["lscd"][month]["mscd"]["g"][game]["stt"] == "Final":
#   print(f'visitor: {obj["lscd"][month]["mscd"]["g"][game]["v"]["ta"]}\nhome: {obj["lscd"][month]["mscd"]["g"][game]["h"]["ta"]}')

teamAbbrvs = ["ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", 
"LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]

teamScores=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
rosterLengths=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
winsOverYears = []
lossesOverYears = []
playoffWinsOverYears = []
playoffLossesOverYears = []
startDates = [20151027, 20161025, 20171017, 20181016, 20191022, 20201222]
for i in range(6):
    winsOverYears.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    lossesOverYears.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    playoffWinsOverYears.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    playoffLossesOverYears.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
teamORTGs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
teamDRTGs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ans = []
model = keras.Sequential()

for year in range(len(winsOverYears)):
    for team in teamAbbrvs:
        winsOverYears[year][teamAbbrvs.index(team)] = 0
        lossesOverYears[year][teamAbbrvs.index(team)] = 0

with open("stats.txt") as fileIn:
    for line in fileIn:
        l = line.strip().split("%")
        player = l[0]
        vorp = float(l[1])
        gp = int(l[2])
        health = l[3]
        ortg = float(l[4])
        drtg = float(l[5])
        if type(vorp) == float and vorp >= 1.5:
            #print(player)
            pogVorpPlayers.append(player)
        playerStatsDict[player] = [vorp, gp, health, ortg, drtg]
    #print(playerStatsDict)


with open("roster.txt") as fileIn:
    for line in fileIn:
        player = line.strip().split("%")[0]
        team = int(line.strip().split("%")[1])
        if player in playerStatsDict:
            allPlayers.append(player)
            playerTeamDict[player] = team
            rosterLengths[team] += 1
    #print(playerTeamDict)
    #print(rosterLengths)


for team in teamAbbrvs:
    pogPlayers.append({})

def get_odds(team1, team2):
    return model.predict([team1, team2, teamScores[team1], teamScores[team2], winsOverYears[5][team1], lossesOverYears[5][team1], winsOverYears[5][team2], 
    lossesOverYears[5][team2], winsOverYears[4][team1], lossesOverYears[4][team1], winsOverYears[4][team2], lossesOverYears[4][team2], teamORTGs[team1],
    teamDRTGs[team1], teamORTGs[team2], teamDRTGs[team2], len(filteredPogPlayers[team1]), len(filteredPogPlayers[team2])][0][0])

def gatherStats(url):
    res = requests.get(url)
    obj = res.json()

    yearIndex = (int(url[57:61]) - 5) % 2010
    #print(yearIndex)
    for month in range(len(obj["lscd"])):
        gameList = obj["lscd"][month]["mscd"]["g"]
        for game in range(len(gameList)):
            gameData = []
            currentGame = gameList[game]
            if currentGame["stt"] == "Final":
                homeAbbrv = currentGame["h"]["ta"]
                awayAbbrv = currentGame["v"]["ta"]
                gameDate = int(currentGame["gcode"][:8])
                if awayAbbrv in teamAbbrvs and homeAbbrv in teamAbbrvs and gameDate >= startDates[yearIndex]:
                    homeInd = teamAbbrvs.index(homeAbbrv)
                    awayInd = teamAbbrvs.index(awayAbbrv)
                    #homeRec = currentGame["h"]["re"]
                    #awayRec = currentGame["v"]["re"]
                    if currentGame["seri"] != "":
                        if float(currentGame["h"]["s"]) > float(currentGame["v"]["s"]):
                            playoffLossesOverYears[yearIndex][awayInd] += float(1)
                            playoffWinsOverYears[yearIndex][homeInd] += float(1)
                        else:
                            playoffWinsOverYears[yearIndex][awayInd] += float(1)
                            playoffLossesOverYears[yearIndex][homeInd] += float(1)

                    else:
                        #homeWins = float(homeRec[:homeRec.index("-")])
                        #homeLosses = float(homeRec[homeRec.index("-") + 1:])
                        #awayWins = float(awayRec[:awayRec.index("-")])
                        #awayLosses = float(awayRec[awayRec.index("-") + 1:])
                        #print(homeRec, homeWins, homeLosses)
                        #print(awayRec, awayWins, awayLosses)

                        if float(currentGame["h"]["s"]) > float(currentGame["v"]["s"]):
                            lossesOverYears[yearIndex][awayInd] += float(1)
                            winsOverYears[yearIndex][homeInd] += float(1)
                        else:
                            winsOverYears[yearIndex][awayInd] += float(1)
                            lossesOverYears[yearIndex][homeInd] += float(1)
                    if yearIndex != 0:
                        ans.append(float(1)) if float(currentGame["h"]["s"]) > float(currentGame["v"]["s"]) else ans.append(float(0))
                        gameData.append(awayInd)
                        gameData.append(homeInd)
                        #gameData.append(float(teamScores[awayInd]))
                        #gameData.append(float(teamScores[homeInd]))
                        #gameData.append(float(currentGame["v"]["s"]))
                        #gameData.append(float(currentGame["h"]["s"]))
                        gameData.append(winsOverYears[yearIndex][awayInd])
                        gameData.append(lossesOverYears[yearIndex][awayInd])
                        gameData.append(winsOverYears[yearIndex][homeInd])
                        gameData.append(lossesOverYears[yearIndex][homeInd])
                        gameData.append(winsOverYears[yearIndex - 1][awayInd])
                        gameData.append(lossesOverYears[yearIndex - 1][awayInd])
                        gameData.append(winsOverYears[yearIndex - 1][homeInd])
                        gameData.append(lossesOverYears[yearIndex - 1][homeInd])
                        gameData.append(playoffWinsOverYears[yearIndex - 1][awayInd])
                        gameData.append(playoffLossesOverYears[yearIndex - 1][awayInd])
                        gameData.append(playoffWinsOverYears[yearIndex - 1][homeInd])
                        gameData.append(playoffLossesOverYears[yearIndex - 1][homeInd])

                        #print(gameData)
                        #time.sleep(0.1)

                        teamScores[awayInd] += float(currentGame["v"]["s"])
                        teamScores[teamAbbrvs.index(homeAbbrv)] += float(currentGame["h"]["s"])

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


def avgRatings():
    for pair in playerTeamDict.items():
        player = pair[0]
        team = pair[1]
        teamORTGs[pair[1]] += playerStatsDict[player][3]
        teamDRTGs[pair[1]] += playerStatsDict[player][4]
    for team in range(len(rosterLengths)):
        teamORTGs[team] /= rosterLengths[team]
        teamDRTGs[team] /= rosterLengths[team]
    


def add_other_stats():
    for gdata in data:
        gdata.append(teamORTGs[gdata[0]])
        gdata.append(teamDRTGs[gdata[0]])
        gdata.append(teamORTGs[gdata[1]])
        gdata.append(teamDRTGs[gdata[1]])
        gdata.append(len(filteredPogPlayers[gdata[0]]))
        gdata.append(len(filteredPogPlayers[gdata[1]]))
        #if gdata[1] == 12:
        #    print(gdata)
        #print(gdata)
        #time.sleep(0.1)

def main():

    model.add(keras.layers.Dense(256, activation="relu",input_shape=(20,)))
    #model.add(keras.layers.Dense(875, input_shape=(256,), activation="relu"))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(1, activation="sigmoid"))

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    for urlInd in range(len(URLs)):
        gatherStats(URLs[urlInd])
    for team in pogPlayers:
        newEntry = dict(filter(lambda elem: (elem[0] in playerStatsDict) and ((elem[0] in pogVorpPlayers) or ((playerStatsDict[elem[0]][2] == "Healthy") and (playerStatsDict[elem[0]][1] > 140) and (elem[1] / playerStatsDict[elem[0]][1] > 0.13))), team.items()))
        filteredPogPlayers.append(newEntry)
    #print(filteredPogPlayers)
    avgRatings()
    add_other_stats()
    #print(winsOverYears)
    #print(lossesOverYears)
    train_ans = tf.convert_to_tensor(ans)
    train_data = tf.convert_to_tensor(data)
    #print(train_ans)
    #print(train_data)
    #print(winsOverYears)
    #print(lossesOverYears)
    #print(ans)
    #train_data = tf.data.Dataset.from_tensor_slices(data)
    #valid_data = tf.data.Dataset.from_tensor_slices(ans)
    #model.fit(data, ans, epochs=50)
    model.fit(train_data, train_ans, epochs=250)
    for i in range(15):
        for j in range(15):
            if i != j:
                print(get_odds(i, j))
    #print(filteredPogPlayers)

if __name__ == "__main__":
    main()