import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

def addrollingform(games, window=10): #rolling win pct and scoring margin per team, shifted so no lookahead
    games=games.sort_values("date").reset_index(drop=True)
    hometeamgames=games[["date","hometeam","homewin"]].rename(columns={"hometeam":"team","homewin":"win"})
    hometeamgames["margin"]=games["homescore"]-games["awayscore"]
    awayteamgames=games[["date","awayteam","homewin"]].rename(columns={"awayteam":"team"})
    awayteamgames["win"]=~awayteamgames["homewin"]
    awayteamgames["margin"]=games["awayscore"]-games["homescore"]
    awayteamgames=awayteamgames.drop(columns="homewin")
    allteamgames=pd.concat([hometeamgames, awayteamgames]).sort_values("date")
    allteamgames["rollingwinpct"]=allteamgames.groupby("team")["win"].transform(lambda x: x.shift(1).rolling(window, min_periods=3).mean())
    allteamgames["rollingmargin"]=allteamgames.groupby("team")["margin"].transform(lambda x: x.shift(1).rolling(window, min_periods=3).mean())
    return allteamgames

def addrestdays(games): #days of rest each team had going into the game
    games=games.sort_values("date").reset_index(drop=True)
    hometeamgames=games[["date","hometeam"]].rename(columns={"hometeam":"team"})
    awayteamgames=games[["date","awayteam"]].rename(columns={"awayteam":"team"})
    allteamgames=pd.concat([hometeamgames, awayteamgames]).sort_values("date")
    allteamgames["lastgame"]=allteamgames.groupby("team")["date"].shift(1)
    allteamgames["restdays"]=(allteamgames["date"]-allteamgames["lastgame"]).dt.days
    games=games.merge(allteamgames[["date","team","restdays"]], left_on=["date","hometeam"], right_on=["date","team"], how="left").rename(columns={"restdays":"homerest"}).drop(columns="team")
    games=games.merge(allteamgames[["date","team","restdays"]], left_on=["date","awayteam"], right_on=["date","team"], how="left").rename(columns={"restdays":"awayrest"}).drop(columns="team")
    games["restdiff"]=games["homerest"]-games["awayrest"]
    return games

def addfeatures(games, window=10): #attaches winpct, margin, elo, and rest features back onto the game table
    from elo import calculateelo
    teamform=addrollingform(games, window)
    games=games.merge(teamform[["date","team","rollingwinpct","rollingmargin"]], left_on=["date","hometeam"], right_on=["date","team"], how="left").rename(columns={"rollingwinpct":"homewinpct","rollingmargin":"homemargin"}).drop(columns="team")
    games=games.merge(teamform[["date","team","rollingwinpct","rollingmargin"]], left_on=["date","awayteam"], right_on=["date","team"], how="left").rename(columns={"rollingwinpct":"awaywinpct","rollingmargin":"awaymargin"}).drop(columns="team")
    games["winpctdiff"]=games["homewinpct"]-games["awaywinpct"]
    games["margindiff"]=games["homemargin"]-games["awaymargin"]
    games=calculateelo(games)
    games=addrestdays(games)
    games=games.dropna(subset=["homewinpct","awaywinpct","homemargin","awaymargin"])
    return games

if __name__ == '__main__':
    from data import getgames
    games=getgames("2025-05-01", "2025-09-30")
    featured=addfeatures(games)
    print(featured[["date","hometeam","awayteam","homewinpct","awaywinpct","winpctdiff","homewin"]].head(15))
    print(f"\nGames with features: {len(featured)}")
