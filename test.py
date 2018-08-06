from nba_py.player import get_player, PlayerList, PlayerSummary, PlayerYearOverYearSplits
from nba_py import Scoreboard
from nba_py.game import Boxscore
from datetime import date

today = date.today()  
scores = Scoreboard(5, 4, 2017, league_id="00")
gameNo = scores.available()
print(gameNo)
#Make an array
length = len(gameNo)
allstats = []
game = [ {0:{}, 1:{}} for x in range(length) ]
teamstats = [ {0:{}, 1:{}} for x in range(length) ]




    #get stats from all games available
    #For every game ....
for i in range(len(gameNo)):    
    gameid = gameNo[i]["GAME_ID"]
    box = Boxscore(gameid)  
    stats = box.team_stats()
    # get name and pts 
    for j in range(len(stats)):
        teamstats[i][j]['name'] = stats[j]["TEAM_ABBREVIATION"]
        teamstats[i][j]['pts'] = stats[j]["PTS"]

        game[i] = teamstats[i]

    allstats.append(game[i])

