import pandas as pd

#standard elo system, every team starts at 1500. updates after each game based on result AND how big the win was
def calculateelo(games, kfactor=20, homeadvantage=75):
    games=games.sort_values("date").reset_index(drop=True)
    elos={}
    homeeloslist=[]
    awayeloslist=[]
    currentseason=None

    for i, game in games.iterrows():
        #regress elo toward the mean a bit at the start of each new season, so one bad year doesn't haunt a team forever
        if game["season"]!=currentseason:
            currentseason=game["season"]
            for team in elos:
                elos[team]=1500+(elos[team]-1500)*0.75
        hometeam=game["hometeam"]
        awayteam=game["awayteam"]
        homeelo=elos.get(hometeam, 1500)
        awayelo=elos.get(awayteam, 1500)
        #save the PRE-game elo, this is what we'll use as a feature, no lookahead
        homeeloslist.append(homeelo)
        awayeloslist.append(awayelo)
        #expected win probability based on the elo gap, includes home court edge
        expectedhome=1/(1+10**(-(homeelo+homeadvantage-awayelo)/400))
        actualhome=1 if game["homewin"] else 0
        #margin of victory multiplier, blowouts move elo more than narrow wins
        margin=abs(game["homescore"]-game["awayscore"])
        elodiff=homeelo - awayelo if actualhome==1 else awayelo - homeelo
        movmultiplier=((margin+3)**0.8) / (7.5 + 0.006*elodiff)
        change=kfactor*movmultiplier*(actualhome-expectedhome)
        elos[hometeam]=homeelo+change
        elos[awayteam]=awayelo-change
    games["homeelo"]=homeeloslist
    games["awayelo"]=awayeloslist
    games["elodiff"]=games["homeelo"]-games["awayelo"]
    return games
