import tensorflow as tf
import numpy as np
from tensorflow import keras
import requests

# http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2020/league/00_full_schedule.json
# http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json


def main():
    res = requests.get("http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/league/00_full_schedule.json")
    print(res.json())


if __name__ == "__main__":
    main()