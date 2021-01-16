import tensorflow as tf
import numpy as np
from tensorflow import keras
import requests
import json

# http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json
# http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json

teamAbbrvs = ["ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", 
"LAC", "LAL", "MEM", "MIA", "MIL", "NOP", "NYK", "OKC", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]

def main():
    res = requests.get("http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json")
    obj = res.json()
    for month in range(len(obj["lscd"])):
        for game in range(len(obj["lscd"][month]["mscd"]["g"])):
            if obj["lscd"][month]["mscd"]["g"][game]["stt"] == "Final":
                print(f'visitor: {obj["lscd"][month]["mscd"]["g"][game]["v"]["ta"]}\nhome: {obj["lscd"][month]["mscd"]["g"][game]["h"]["ta"]}')



if __name__ == "__main__":
    main()