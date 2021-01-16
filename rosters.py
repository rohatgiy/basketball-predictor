import requests
import json

# https://raw.githubusercontent.com/alexnoob/BasketBall-GM-Rosters/master/2020-21.NBA.Roster.json


playerTeamList = []
#print(len(teamAbbrvs))
def main():
    res = requests.get("https://raw.githubusercontent.com/alexnoob/BasketBall-GM-Rosters/master/2020-21.NBA.Roster.json")
    obj = res.json()
    #print(obj["players"][0])
    for playerInd in range(len(obj["players"])):
        player = obj["players"][playerInd]
        playerName = ""
        #print(player["tid"])
        if player["tid"] >= 0:
            if "name" not in player:
                playerName = player["firstName"] + ' ' + player["lastName"]
            else:
                playerName = player["name"]
            s = f'{playerName}%{player["tid"]}\n'
            #print(s)
            playerTeamList.append(s)

    with open("roster.txt", "w") as fileOut:
        fileOut.writelines(playerTeamList)
    #print(playerTeamList)


if __name__ == "__main__":
    main()