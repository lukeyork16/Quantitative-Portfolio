import requests
import pandas as pd

def getscoreboard(date): #pulls the wnba scoreboard for a given date
    url=f"https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard?dates={date}"
    response=requests.get(url)
    data=response.json()
    return data

def getgames(startdate, enddate): #pulls games across a date range into one table
    dates=pd.date_range(startdate, enddate)
    allgames=[]
    for date in dates:
        datestr=date.strftime("%Y%m%d")
        data=getscoreboard(datestr)
        for event in data.get("events", []):
            competition=event["competitions"][0]
            teams=competition["competitors"]
            hometeam=next(t for t in teams if t["homeAway"]=="home")
            awayteam=next(t for t in teams if t["homeAway"]=="away")
            allgames.append({
                "date": date,
                "hometeam": hometeam["team"]["displayName"],
                "awayteam": awayteam["team"]["displayName"],
                "homescore": int(hometeam.get("score",0)),
                "awayscore": int(awayteam.get("score",0)),
                "homewin": int(hometeam.get("score",0)) > int(awayteam.get("score",0)),
            })
    return pd.DataFrame(allgames)

def getmultipleseasons(seasons): #pulls several seasons at once, tags each with its year
    allseasons=[]
    for year in seasons:
        games=getgames(f"{year}-05-01", f"{year}-09-30")
        games["season"]=year
        allseasons.append(games)
    return pd.concat(allseasons).reset_index(drop=True)

if __name__ == '__main__':
    df=getgames("2025-05-01", "2025-09-30")
    print(df.head(10))
    print(f"\nTotal games found: {len(df)}")
