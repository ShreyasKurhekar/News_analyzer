import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from fetch_new import fetch_news
from process_news import process_news
from visualize import plot_all

BASE_DIR = Path(__file__).resolve().parent
NEWS_FILE = BASE_DIR / "data" / "news.json"


def _load_articles():
    if not NEWS_FILE.exists():
        return []

    with NEWS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def _format_timestamp(timestamp):
    if not timestamp:
        return "Time unavailable"

    try:
        published = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return published.strftime("%d %b %Y, %I:%M %p UTC")
    except ValueError:
        return "Time unavailable"


def _build_article_summary(articles, sentiments):
    normalized_articles = []
    sources = []
    valid_times = []

    for index, article in enumerate(articles):
        source_name = article.get("source", {}).get("name") or "Unknown source"
        title = (article.get("title") or "Untitled article").strip()
        description = (article.get("description") or "No summary was provided for this article.").strip()
        published_at = article.get("publishedAt")
        article_url = article.get("url") or "#"

        sources.append(source_name)
        if published_at:
            valid_times.append(published_at)

        sentiment_value = sentiments[index] if index < len(sentiments) else 0
        if sentiment_value > 0.1:
            sentiment_label = "Positive"
        elif sentiment_value < -0.1:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        normalized_articles.append(
            {
                "title": title,
                "description": description,
                "source": source_name,
                "published_at": _format_timestamp(published_at),
                "url": article_url,
                "sentiment_label": sentiment_label,
            }
        )

    source_counts = Counter(sources)
    top_source = source_counts.most_common(1)[0][0] if source_counts else "Unavailable"
    coverage_window = "Live snapshot"
    if valid_times:
        ordered = sorted(valid_times)
        coverage_window = f"{_format_timestamp(ordered[0])} to {_format_timestamp(ordered[-1])}"

    return {
        "articles": normalized_articles[:6],
        "source_count": len(source_counts),
        "top_source": top_source,
        "coverage_window": coverage_window,
    }

def run_analysis(query="india"):
    print("Fetching news...\n")
    if not fetch_news(query):
        print("Stopping because news could not be fetched.")
        return None

    print("Processing news...\n")
    keywords, sentiments = process_news()

    if not keywords:
        print("Stopping because there is no processed data to visualize.")
        return None

    print("Top Keywords:", keywords)
    articles = _load_articles()
    output_file = plot_all(keywords, sentiments)
    return {
        "keywords": keywords,
        "sentiments": sentiments,
        "output_file": str(output_file),
        "query": query,
        "summary": _build_article_summary(articles, sentiments),
    }


def main():
    run_analysis()

if __name__ == "__main__":
    main()
