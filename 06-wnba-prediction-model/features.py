import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
#builds a rolling win percentage for each team, as of right before each game (no lookahead)
def addrollingwinpct(games, window=10):
    games = games.sort_values("date").reset_index(drop=True)

    #stack home and away into one long list of "team played on this date, did they win"
    hometeamgames = games[["date","hometeam","homewin"]].rename(columns={"hometeam":"team","homewin":"win"})
    awayteamgames = games[["date","awayteam","homewin"]].rename(columns={"awayteam":"team"})
    awayteamgames["win"] = ~awayteamgames["homewin"]
    awayteamgames = awayteamgames.drop(columns="homewin")

    alltteamgames = pd.concat([hometeamgames, awayteamgames]).sort_values("date")

    #rolling win pct per team, shifted so it only uses games strictly before the current one
    alltteamgames["rollingwinpct"] = alltteamgames.groupby("team")["win"].transform(
        lambda x: x.shift(1).rolling(window, min_periods=3).mean()
    )

    return alltteamgames

#attaches each team's rolling win pct back onto the original game-level table
def addfeatures(games, window=10):
    teamform=addrollingwinpct(games, window)

    games=games.merge(
        teamform[["date","team","rollingwinpct"]],
        left_on=["date","hometeam"], right_on=["date","team"], how="left"
    ).rename(columns={"rollingwinpct":"homewinpct"}).drop(columns="team")

    games=games.merge(
        teamform[["date","team","rollingwinpct"]],
        left_on=["date","awayteam"], right_on=["date","team"], how="left"
    ).rename(columns={"rollingwinpct":"awaywinpct"}).drop(columns="team")

    #the actual predictive feature: the gap in recent form between the two teams
    games["winpctdiff"]=games["homewinpct"]-games["awaywinpct"]

    #drop early-season games where a team doesn't have enough history yet for a reliable rolling pct
    games=games.dropna(subset=["homewinpct","awaywinpct"])

    return games


if __name__ == '__main__':
    from data import getgames

    games=getgames("2025-05-01", "2025-09-30")
    featured=addfeatures(games)

    print(featured[["date","hometeam","awayteam","homewinpct","awaywinpct","winpctdiff","homewin"]].head(15))
    print(f"\nGames with features: {len(featured)}")
