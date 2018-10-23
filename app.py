import os
import sys
import json
import requests
import datetime
import nba_py
from datetime import date
from nba_py import Scoreboard
from nba_py.game import Boxscore
from nba_py.team import TeamSummary
from nba_py.player import get_player, PlayerList, PlayerSummary, PlayerYearOverYearSplits

from flask import Flask, jsonify, render_template, request, session

#Calculate age using DateTime
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

#Configure application
app = Flask(__name__)

#Set secret key
app.secret_key = 'secret'


@app.route('/', methods=["GET", "POST"]) 
def home():
    """main page"""
    if request.method == 'POST':
        aDate = request.form.get("date")
        today = aDate.split()
        today = today[:6]
        today = " ".join(today)

        today = datetime.datetime.strptime(today, "%a %b %d %Y %X %Z%z")

    else:
        today = date.today()
    scores = Scoreboard(today.month, today.day, today.year, league_id="00")
    gameNo = scores.available()

    if not gameNo:
        scores = Scoreboard(today.month, today.day, today.year, league_id="01")
        gameNo = scores.available() 
    #Dynamic array for number of games
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
        if len(stats) == 0:
            length = 0;
        # get name and pts 
        for j in range(len(stats)):
            teamstats[i][j]['name'] = stats[j]["TEAM_ABBREVIATION"]
            teamstats[i][j]['pts'] = stats[j]["PTS"]

            game[i] = teamstats[i]

        allstats.append(game[i])
    
    return render_template ("mainpage.html", gameNum=length, allstats=allstats, date=today, gameId=gameNo)


@app.route('/search', methods=["GET", "POST"])
def search():
    """Search for the player name"""
    if not request.form.get("q"):
        error = 'Please input name'
    else:
        name = request.form.get("q").split()
        if len(name) > 1:
            first = name[0]
            last = name[1]
        else:
            first = name[0]
            last = None
        #Use nba_py api to get summary of player
        playerid = get_player(first, last, just_id=True)
        session["playerid"] = playerid
        summary = PlayerSummary(playerid)
        sum = summary.info()[0]
        stats = summary.headline_stats()[0]
        p = sum["DISPLAY_FIRST_LAST"]
        #wikipedia summary
        wiki = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/%s" %p)
        wiki = wiki.json()
        #picture headshot
        pic = ("https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/%s" %playerid) + ".png"
        #picture logo
        tabv = summary.info()[0]["TEAM_ABBREVIATION"]
        logo = ("https://stats.nba.com/media/img/teams/logos/%s" %tabv) + "_logo.svg"
        #Datetime to date only
        date = summary.info()[0]["BIRTHDATE"]
        date = date[:10]
        #convert to datetime type
        dob = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        #calculate age
        age = calculate_age(dob)
        #convert PIE
        if "PIE" in stats:
            pie = float((stats["PIE"]) * 100)
        else:
            pie = '-'
        return render_template ("id.html", sum=sum, stats=stats, wiki=wiki, pic=pic, logo=logo, age=age, dob=dob, pie=pie)



@app.route('/game/<gId>', methods=['GET'])
def game(gId):
    """Get boxscore for game"""
    if request.method == "GET":
        session["gameId"] = gId
        box = Boxscore(gId)
        stats = box.player_stats()
        team1 = stats[0]["TEAM_ID"]
        i = 12
        for i in range(len(stats)):
            team2 = stats[i]["TEAM_ID"]
            if team1 != team2:
                break
        name1 = TeamSummary(team1)
        name2 = TeamSummary(team2)
        tn1 = name1.info()[0]["TEAM_CITY"] + " " + name1.info()[0]["TEAM_NAME"]
        tn2 = name2.info()[0]["TEAM_CITY"] + " " + name2.info()[0]["TEAM_NAME"]

        return render_template("game.html", tn1=tn1, tn2=tn2)


@app.route('/gametable')
def gametable():
    """Table stats for /game"""
    gameId = session["gameId"]
    box = Boxscore(gameId)
    stats = box.player_stats()
    #Sort both teams into different arrays
    team1 = []
    team2 = []
    tId = stats[0]["TEAM_ID"]
    for i in range(len(stats)):
        if tId == stats[i]["TEAM_ID"]:
            team1.append(stats[i])
        else:
            team2.append(stats[i])

    return jsonify([team1,team2])

@app.route('/table')
def table():
    """Table staats for /search"""
    playerid = session.get("playerid",None)
    table = PlayerYearOverYearSplits(playerid)
    data = table.by_year()
    return jsonify({"data": data})
   

@app.route('/playerlist')
def plist():
    """Get list of player names for Typeahead to use"""
    plist = PlayerList(league_id='00', only_current=0)
    playerlist = plist.info()
    length = len(playerlist)
    names = []
    for i in range(length):
        names.append(playerlist[i]['DISPLAY_FIRST_LAST'])

    return jsonify(names)



if __name__ == '__main__':
    app.run()