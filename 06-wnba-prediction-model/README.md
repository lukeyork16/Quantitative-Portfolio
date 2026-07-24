# WNBA Win Probability Model

## Overview
A logistic regression model that predicts WNBA game win probabilities using team form, scoring margin, Elo ratings, and rest days. Validated with walk-forward cross-validation across multiple seasons and benchmarked against naive baselines. Includes a full PDF report covering methodology, results, and calibration.

## Key Concepts
- Elo rating system with margin-of-victory weighting and season-to-season regression
- Rolling team form (win %, scoring margin) and rest-day tracking, all computed with no lookahead bias
- Walk-forward cross-validation (always trains on seasons strictly before the test season)
- Baseline comparison: home-team-always-wins vs. Elo-only vs. full model
- Model evaluation: accuracy, log loss, Brier score, and probability calibration
- Automated PDF report generation

## Tools & Libraries
Python, pandas, NumPy, scikit-learn, matplotlib, reportlab, requests

## Files
| File | Purpose |
|---|---|
| `data.py` | Pulls WNBA game results from ESPN's public data feed, across single or multiple seasons |
| `elo.py` | Computes Elo ratings for every team, game by game |
| `features.py` | Builds rolling win %, scoring margin, rest days, and merges in Elo |
| `model.py` | Trains the logistic regression, runs walk-forward validation, saves the final model |
| `evaluation.py` | Log loss, Brier score, and calibration table |
| `report.py` | Generates a full PDF report (methodology, results, calibration chart, limitations) |

## Results
Full model beats a naive "home team always wins" baseline by 10-13 percentage points across every tested season (2023-2025), and modestly outperforms Elo alone in most seasons. Out-of-sample 2025 accuracy: 66.7%, with log loss and Brier score both meaningfully better than a pure-guessing baseline. See `wnba_model_report.pdf` for full details, including an honest breakdown of calibration limits and where the model's edge actually comes from.

## Status
✅ Complete — data pipeline, Elo system, feature engineering, model training with walk-forward validation, evaluation metrics, and the PDF report are all built and tested.

## How to Predict Upcoming Games

The saved model (`wnbamodel.pkl`) expects four features for any matchup: `winpctdiff`, `margindiff`, `elodiff`, `restdiff` — the same features it was trained on, computed as of right before the game being predicted.

Create `predict.py`:

```python
import pandas as pd
from data import getmultipleseasons
from features import addfeatures
from model import loadmodel

def predictupcoming(hometeam, awayteam, gamedate, seasons=[2023,2024,2025]): #predicts a future matchup using each team's most recent stats
    rawgames=getmultipleseasons(seasons) #pull recent history to compute current form/elo/rest
    data=addfeatures(rawgames)
    hometeamrows=data[(data["hometeam"]==hometeam)|(data["awayteam"]==hometeam)].sort_values("date")
    awayteamrows=data[(data["hometeam"]==awayteam)|(data["awayteam"]==awayteam)].sort_values("date")
    homelast=hometeamrows.iloc[-1] #most recent game each team played, to grab their latest stats
    awaylast=awayteamrows.iloc[-1]
    homeelo=homelast["homeelo"] if homelast["hometeam"]==hometeam else homelast["awayelo"]
    awayelo=awaylast["homeelo"] if awaylast["hometeam"]==awayteam else awaylast["awayelo"]
    homewinpct=homelast["homewinpct"] if homelast["hometeam"]==hometeam else homelast["awaywinpct"]
    awaywinpct=awaylast["homewinpct"] if awaylast["hometeam"]==awayteam else awaylast["awaywinpct"]
    homemargin=homelast["homemargin"] if homelast["hometeam"]==hometeam else homelast["awaymargin"]
    awaymargin=awaylast["homemargin"] if awaylast["hometeam"]==awayteam else awaylast["awaymargin"]
    features=pd.DataFrame([{
        "winpctdiff": homewinpct-awaywinpct,
        "margindiff": homemargin-awaymargin,
        "elodiff": homeelo-awayelo,
        "restdiff": 0, #assume even rest unless you know the actual schedule gap
    }])
    model=loadmodel()
    prob=model.predict_proba(features)[0][1]
    print(f"{hometeam} vs {awayteam}: {hometeam} win probability = {prob:.1%}")
    return prob

if __name__ == '__main__':
    predictupcoming("Las Vegas Aces", "New York Liberty", "2026-06-15")
```

Run it:
python predict.py

Update the team names and swap in `restdiff` manually if you know the actual rest gap for that specific matchup (positive if the home team has had more days off, negative if the away team has). This pulls each team's most recent Elo, win %, and margin from the last games in your dataset — for genuinely live use during an active season, re-run `getmultipleseasons` with the current season included so it picks up the latest results.

## How to Regenerate the Report
pip install pandas numpy scikit-learn matplotlib reportlab requests
python report.py

Outputs `wnba_model_report.pdf` in the same folder.

## Notes & Limitations
- Does not account for player-level information (injuries, star player availability), which materially affects real outcomes.
- Calibration in several confidence bins is based on fewer than 30 games more seasons of data would tighten this.
- Claude AI used to create report, along with debug and fix grammar issues.
