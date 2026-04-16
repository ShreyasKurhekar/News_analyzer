import json
from collections import Counter
from pathlib import Path
import re

from textblob import TextBlob

BASE_DIR = Path(__file__).resolve().parent
NEWS_FILE = BASE_DIR / "data" / "news.json"

COMMON_STOPWORDS = {
    "the", "is", "in", "and", "to", "of", "for", "on", "with", "at",
    "by", "from", "a", "an", "this", "that", "it", "as", "are", "be",
    "was", "were", "or", "but", "if", "into", "about", "after", "before",
    "over", "under", "than", "then", "their", "his", "her", "its", "they",
    "them", "you", "your", "our", "ours", "has", "have", "had", "will",
    "would", "can", "could", "should", "may", "might", "not", "more",
    "most", "less", "least", "new", "news", "live", "latest", "update",
}

NEWS_FILLER_WORDS = {
    "says", "say", "said", "reuters", "watch", "photos", "video", "today",
    "tomorrow", "yesterday", "breaking", "report", "reports", "reportedly",
    "amid", "after", "before", "during", "here", "why", "what", "when",
    "where", "how", "who", "explained", "analysis", "recap", "minute",
    "minutes", "week", "weeks", "month", "months", "year", "years",
    "headline", "headlines", "story", "stories", "coverage", "media",
    "read", "reads", "reading", "told", "according", "via", "makes",
    "make", "made", "take", "takes", "latest", "updates",
}


def _tokenize_news_text(text):
    cleaned = re.sub(r"[^a-zA-Z ]", " ", text).lower()
    return [word for word in cleaned.split() if len(word) > 2]


def _is_meaningful_term(word):
    return word not in COMMON_STOPWORDS and word not in NEWS_FILLER_WORDS

def process_news():
    if not NEWS_FILE.exists():
        print("No news data found. Please fetch news first.")
        return [], []

    with NEWS_FILE.open("r", encoding="utf-8") as f:
        articles = json.load(f)

    words = []
    sentiments = []

    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        if title:
            blob = TextBlob(title)
            sentiments.append(blob.sentiment.polarity)

            words.extend(_tokenize_news_text(title))
            if description:
                words.extend(_tokenize_news_text(description))

    filtered = [word for word in words if _is_meaningful_term(word)]

    return Counter(filtered).most_common(10), sentiments
