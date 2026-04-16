# visualize.py

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def plot_all(keywords, sentiments):
    if not keywords:
        print("No data to plot!")
        return

    # --- Keyword Data ---
    words = [x[0] for x in keywords]
    counts = [x[1] for x in keywords]

    # --- Sentiment Data ---
    pos = sum(1 for s in sentiments if s > 0)
    neg = sum(1 for s in sentiments if s < 0)
    neu = sum(1 for s in sentiments if s == 0)

    labels = ['Positive', 'Negative', 'Neutral']
    values = [pos, neg, neu]

    # --- Create subplots ---
    plt.figure(figsize=(12, 5))

    # Bar chart (left)
    plt.subplot(1, 2, 1)
    plt.bar(words, counts)
    plt.title("Top Keywords")
    plt.xticks(rotation=45)

    # Pie chart (right)
    plt.subplot(1, 2, 2)
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Sentiment Analysis")

    plt.tight_layout()
    DATA_DIR.mkdir(exist_ok=True)
    output_file = DATA_DIR / "output.png"
    plt.savefig(output_file)
    plt.close()
    return output_file
