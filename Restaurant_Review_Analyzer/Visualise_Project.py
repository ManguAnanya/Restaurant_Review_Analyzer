import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

def plot_score_distribution(df):
    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(df['Average_Rating'], bins=10, kde=False, ax=ax, color="skyblue")
    ax.set_title("Review Score Distribution")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Count")
    return fig

def plot_sentiment_distribution(df):
    fig, ax = plt.subplots()
    df['Sentiment'].value_counts().plot(kind='pie', autopct='%1.0f%%', ax=ax)
    ax.set_ylabel("")
    ax.set_title("Sentiment Breakdown")
    return fig

def generate_wordcloud(df, sentiment):
    text = " ".join(df[df['Sentiment'] == sentiment]['review_text'].dropna())
    if not text.strip():
        text = "No reviews available"
    wc = WordCloud(width=600, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    ax.set_title(f"{sentiment} Review Word Cloud")
    return fig
