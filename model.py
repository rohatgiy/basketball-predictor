import tensorflow as tf
import numpy as np
from tensorflow import keras
import requests
import json

# http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json
# http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json

# if obj["lscd"][month]["mscd"]["g"][game]["stt"] == "Final":
#   print(f'visitor: {obj["lscd"][month]["mscd"]["g"][game]["v"]["ta"]}\nhome: {obj["lscd"][month]["mscd"]["g"][game]["h"]["ta"]}')

teamAbbrvs = ["ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", 
"LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]

pogplayers = []

for team in teamAbbrvs:
    pogplayers.append({team:{}})

model = keras.Sequential()

model.add(keras.layers.Dense(256,input_shape=(6,), activation="relu"))
model.add(keras.layers.Dense(875, input_shape=(256,), activation="relu"))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(1, activation="sigmoid"))

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])


def main():
    res = requests.get("http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json")
    obj = res.json()
    for month in range(len(obj["lscd"])):
        for game in range(len(obj["lscd"][month]["mscd"]["g"])):
            highScorers = obj["lscd"][month]["mscd"]["g"][game]["ptsls"]["pl"]
            for player in highScorers:
                playerFullName = player["fn"] + ' ' + player["ln"]
                #print(player["ta"])
                if player["ta"] in teamAbbrvs:
                    playerTeamIndex = teamAbbrvs.index(player["ta"])

                    if playerFullName not in pogplayers[playerTeamIndex][player["ta"]]:
                        pogplayers[playerTeamIndex][player["ta"]][playerFullName] = 1
                    else :
                        pogplayers[playerTeamIndex][player["ta"]][playerFullName] += 1
    print(pogplayers)

if __name__ == "__main__":
    get_odds("LAL", "NOP")