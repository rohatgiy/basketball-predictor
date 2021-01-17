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
        latestseason = 0
        gamesPlayed = 0
        ovrORTG = 0
        ovrDRTG = 0
        #print(player["tid"])
        if player["tid"] >= 0:
            if "stats" in player:
                if "injury" in player:
                    playerHealth = player["injury"]["type"]
                for season in player["stats"]:
                    if season["season"] >= 2016 and season["season"] < 2021:
                        gamesPlayed += season["gp"]
                        #print(year["season"])
                        if season["season"] == 2020:
                            if "ortg" in season:
                                ovrORTG += season["ortg"]
                                ovrDRTG += season["drtg"]
                            if "vorp" in season:
                                #print(year["vorp"])
                                playerVORP += season["vorp"]
                                #print(playerVORP)
                                latestseason += 1
                        #print(playerVORP)
                playerAvgVORP = 0
                avgORTG = 0
                avgDRTG = 0
                #if type(playerVORP) == int or type(playerVORP) == float:
                if latestseason > 0:
                    avgORTG = ovrORTG / latestseason
                    avgDRTG = ovrDRTG / latestseason
                    playerAvgVORP = playerVORP / latestseason
                
                
                if "name" not in player:
                    playerName = player["firstName"] + ' ' + player["lastName"]
                else:
                    playerName = player["name"]
                s = f'{playerName}%{playerAvgVORP}%{gamesPlayed}%{playerHealth}%{avgORTG}%{avgDRTG}\n'
                #print(s)
                playerStatList.append(s)
            
    with open("stats.txt", "w") as fileOut:
        fileOut.writelines(playerStatList)
    #print(playerTeamList)


if __name__ == "__main__":
    main()