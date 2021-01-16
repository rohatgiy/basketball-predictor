import requests
import json

# https://raw.githubusercontent.com/alexnoob/BasketBall-GM-Rosters/master/2020-21.NBA.Roster.json

teamAbbrvs = ["ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", 
"LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]
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
            
            playerTeamList.append(f'{teamAbbrvs[player["tid"]]} - {playerName}')
print(playerTeamList)


if __name__ == "__main__":
    main()