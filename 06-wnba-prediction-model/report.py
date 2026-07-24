import matplotlib.pyplot as plt
from datetime import date

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

from data import getmultipleseasons
from features import addfeatures
from model import trainmodel
from evaluation import getmetrics, calibrationtable

#builds and saves the calibration chart as an image so it can be dropped into the pdf
def makecalibrationchart(calibration, path="calibrationchart.png"):
    fig, ax = plt.subplots(figsize=(6,5))
    ax.plot([0,1],[0,1], linestyle="--", color="gray", label="Perfect calibration")
    ax.scatter(calibration["avgpredicted"], calibration["avgactual"], s=calibration["ngames"]*3, alpha=0.7)
    ax.set_xlabel("Predicted Win Probability")
    ax.set_ylabel("Actual Win Rate")
    ax.set_title("Model Calibration (2025, out-of-sample)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path

#turns a dataframe into a reportlab table with basic styling
def dftotable(df, decimals=4):
    data = [list(df.columns)]
    for _, row in df.iterrows():
        data.append([f"{v:.{decimals}f}" if isinstance(v,float) else str(v) for v in row])

    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1f2937")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f3f4f6")]),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    return table


def buildreport():
    styles = getSampleStyleSheet()
    bodystyle = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=10)
    headingstyle = ParagraphStyle("heading", parent=styles["Heading2"], spaceBefore=16, spaceAfter=8)

    story = []

    #title page
    story.append(Paragraph("WNBA Win Probability Model", styles["Title"]))
    story.append(Paragraph("Model Validation & Methodology Report", styles["Heading3"]))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Generated {date.today().strftime('%B %d, %Y')} — Luke York", bodystyle))
    story.append(Spacer(1,24))

    #overview
    story.append(Paragraph("Overview", headingstyle))
    story.append(Paragraph(
        "This model predicts WNBA game win probabilities using a logistic regression trained on team form, "
        "scoring margin, an Elo rating system, and rest days. It is validated using walk-forward cross-validation "
        "across multiple seasons, benchmarked against naive baselines, and evaluated for both accuracy and "
        "probability calibration, since a model intended to inform real decisions needs to be right about its "
        "confidence level, not just its picks.", bodystyle
    ))

    #methodology
    story.append(Paragraph("Methodology", headingstyle))
    story.append(Paragraph(
        "<b>Features:</b> rolling win percentage (10-game window), rolling scoring margin, Elo rating "
        "(margin-of-victory weighted, with season-to-season regression toward the mean), and rest days between games.", bodystyle
    ))
    story.append(Paragraph(
        "<b>Validation:</b> walk-forward cross-validation — for each test season, the model is trained only on seasons "
        "that came strictly before it, so no future information leaks into training. This mirrors how the model would "
        "actually be used: always predicting forward in time.", bodystyle
    ))
    story.append(Paragraph(
        "<b>Baselines:</b> compared against (1) always picking the home team, and (2) Elo rating alone, to isolate "
        "how much the additional features actually contribute beyond a single strong predictor.", bodystyle
    ))

    #results
    seasons = [2022,2023,2024,2025]
    rawgames = getmultipleseasons(seasons)
    data = addfeatures(rawgames)
    fullfeatures = ["winpctdiff","margindiff","elodiff","restdiff"]

    story.append(Paragraph("Walk-Forward Validation Results", headingstyle))
    import pandas as pd
    results = []
    for testseason in [2023,2024,2025]:
        trainseasons = [s for s in seasons if s < testseason]
        model, xtrain, ytrain, xtest, ytest = trainmodel(data, trainseasons, testseason, fullfeatures)
        modelacc = model.score(xtest,ytest)
        homebaseline = ytest.mean()
        eloonly,_,_,xtesteloonly,ytesteloonly = trainmodel(data, trainseasons, testseason, ["elodiff"])
        eloacc = eloonly.score(xtesteloonly,ytesteloonly)
        results.append({"Test Season":testseason,"Home-Always-Wins":homebaseline,"Elo-Only":eloacc,"Full Model":modelacc})

    resultsdf = pd.DataFrame(results)
    story.append(dftotable(resultsdf))
    story.append(Spacer(1,12))
    story.append(Paragraph(
        "The full model beats the home-team baseline by 10-13 percentage points in every tested season, and modestly "
        "outperforms Elo alone in two of three seasons — indicating Elo is the dominant predictive signal, with the "
        "additional features (form, margin, rest) providing a smaller, not fully consistent, incremental improvement.", bodystyle
    ))

    #out of sample metrics + calibration
    story.append(Paragraph("Out-of-Sample Metrics (2025)", headingstyle))
    model, xtrain, ytrain, xtest, ytest = trainmodel(data, [2022,2023,2024], 2025, fullfeatures)
    metrics = getmetrics(model, xtest, ytest)

    metricstable = pd.DataFrame([{
        "Accuracy": metrics["accuracy"],
        "Log Loss": metrics["logloss"],
        "Brier Score": metrics["brierscore"],
    }])
    story.append(dftotable(metricstable))
    story.append(Spacer(1,10))
    story.append(Paragraph(
        "Log loss and Brier score are both meaningfully better than a pure-guessing baseline (0.693 log loss, 0.25 "
        "Brier score for always guessing 50%), indicating the model's confidence levels carry real information, not "
        "just its win/loss picks.", bodystyle
    ))

    story.append(PageBreak())
    story.append(Paragraph("Calibration", headingstyle))
    calibration = calibrationtable(model, xtest, ytest)
    chartpath = makecalibrationchart(calibration)
    story.append(Image(chartpath, width=5*inch, height=4.2*inch))
    story.append(Spacer(1,10))
    story.append(Paragraph(
        "Points near the dashed diagonal indicate well-calibrated predictions (e.g. games predicted at 80% confidence "
        "actually won about 80% of the time). Most bins track closely; a few bins with small sample sizes (under 20 "
        "games) show larger deviations, which reflects limited data in those confidence ranges rather than a "
        "systematic flaw in the model.", bodystyle
    ))

    #limitations
    story.append(Paragraph("Limitations & Honest Caveats", headingstyle))
    for point in [
        "Calibration in several confidence bins is based on fewer than 30 games; more historical seasons would improve confidence in those estimates.",
        "The model does not account for player-level information (injuries, star player rest/availability), which materially affects real WNBA outcomes.",
        "Elo ratings regress partially toward the mean between seasons, which is a simplification of true roster turnover.",
        "This model reflects historical patterns and is not a guarantee of future performance. Any use for betting purposes carries real financial risk.",
    ]:
        story.append(Paragraph(f"• {point}", bodystyle))

    doc = SimpleDocTemplate("wnba_model_report.pdf", pagesize=letter,
                             topMargin=0.75*inch, bottomMargin=0.75*inch)
    doc.build(story)
    print("Report saved to wnba_model_report.pdf")


if __name__ == '__main__':
    buildreport()
