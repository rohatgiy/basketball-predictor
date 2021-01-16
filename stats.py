import requests
import json

# https://raw.githubusercontent.com/alexnoob/BasketBall-GM-Rosters/master/2020-21.NBA.Roster.json


playerStatList = []
#print(len(teamAbbrvs))
def main():
    res = requests.get("https://raw.githubusercontent.com/alexnoob/BasketBall-GM-Rosters/master/2020-21.NBA.Roster.json")
    obj = res.json()
    #print(obj["players"][0])
    for playerInd in range(len(obj["players"])):
        player = obj["players"][playerInd]
        playerName = "N/A"
        playerVORP = 0
        seasons = 0
        gamesPlayed = 0
        #print(player["tid"])
        if player["tid"] >= 0:
            if "stats" in player:
                if "injury" in player:
                    playerHealth = player["injury"]["type"]
                for season in player["stats"]:
                    if season["season"] >= 2015:
                        gamesPlayed += season["gp"]
                        #print(year["season"])
                        if season["season"] == 2020:
                            if "vorp" in season:
                                #print(year["vorp"])
                                playerVORP += season["vorp"]
                                #print(playerVORP)
                                seasons += 1
                        print(playerVORP)
                playerAvgVORP = 0
                #if type(playerVORP) == int or type(playerVORP) == float:
                if seasons > 0:
                    playerAvgVORP = playerVORP/seasons
                
                
                if "name" not in player:
                    playerName = player["firstName"] + ' ' + player["lastName"]
                else:
                    playerName = player["name"]
                s = f'{playerName}%{playerAvgVORP}%{gamesPlayed}%{playerHealth}\n'
                #print(s)
                playerStatList.append(s)

    with open("stats.txt", "w") as fileOut:
        fileOut.writelines(playerStatList)
    #print(playerTeamList)


if __name__ == "__main__":
    main()