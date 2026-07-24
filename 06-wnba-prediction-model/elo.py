import pandas as pd

def calculateelo(games, kfactor=20, homeadvantage=75): #standard elo, every team starts at 1500, updates based on result and margin
    games=games.sort_values("date").reset_index(drop=True)
    elos={}
    homeeloslist=[]
    awayeloslist=[]
    currentseason=None
    for i, game in games.iterrows():
        if game["season"]!=currentseason: #regress elo toward the mean each new season so one bad year doesn't stick forever
            currentseason=game["season"]
            for team in elos:
                elos[team]=1500+(elos[team]-1500)*0.75
        hometeam=game["hometeam"]
        awayteam=game["awayteam"]
        homeelo=elos.get(hometeam, 1500)
        awayelo=elos.get(awayteam, 1500)
        homeeloslist.append(homeelo) #save pre-game elo, no lookahead
        awayeloslist.append(awayelo)
        expectedhome=1/(1+10**(-(homeelo+homeadvantage-awayelo)/400)) #win prob based on elo gap plus home edge
        actualhome=1 if game["homewin"] else 0
        margin=abs(game["homescore"]-game["awayscore"])
        elodiff=homeelo-awayelo if actualhome==1 else awayelo-homeelo
        movmultiplier=((margin+3)**0.8)/(7.5+0.006*elodiff) #blowouts move elo more than close wins
        change=kfactor*movmultiplier*(actualhome-expectedhome)
        elos[hometeam]=homeelo+change
        elos[awayteam]=awayelo-change
    games["homeelo"]=homeeloslist
    games["awayelo"]=awayeloslist
    games["elodiff"]=games["homeelo"]-games["awayelo"]
    return games
