from pathlib import Path

from flask import Flask, render_template, request, send_from_directory, url_for

from main import run_analysis

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


@app.route("/", methods=["GET", "POST"])
def index():
    context = {
        "error": None,
        "keywords": [],
        "sentiment_summary": None,
        "query": "india",
        "chart_url": None,
        "summary": None,
    }

    if request.method == "POST":
        query = request.form.get("query", "india").strip() or "india"
        context["query"] = query

        result = run_analysis(query)
        if not result:
            context["error"] = "News analysis could not be completed. Please try again."
            return render_template("index.html", **context)

        sentiments = result["sentiments"]
        context["keywords"] = result["keywords"]
        context["chart_url"] = url_for("generated_file", filename="output.png")
        context["summary"] = result.get("summary")
        average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        context["sentiment_summary"] = {
            "positive": sum(1 for value in sentiments if value > 0),
            "negative": sum(1 for value in sentiments if value < 0),
            "neutral": sum(1 for value in sentiments if value == 0),
            "total": len(sentiments),
            "average": round(average_sentiment, 2),
        }

    return render_template("index.html", **context)


@app.route("/generated/<path:filename>")
def generated_file(filename):
    return send_from_directory(DATA_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
