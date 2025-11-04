import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

def plot_score_distribution(df, search_query=None):
    # Filter dataframe based on search query if provided
    if search_query:
        df = df[df['Restaurant_Name'].str.contains(search_query, case=False, na=False)]

    fig, ax = plt.subplots(figsize=(7,4))

    # If there are matching restaurants, plot their ratings individually
    if not df.empty:
        sns.barplot(
            x='Restaurant_Name',
            y='Average_Rating',
            data=df,
            palette='viridis',
            ax=ax
        )
        ax.set_title(f"Ratings for Restaurants Matching '{search_query}'")
        ax.set_xlabel("Restaurant Name")
        ax.set_ylabel("Average Rating")
        ax.tick_params(axis='x', rotation=45)
    else:
        ax.text(0.5, 0.5, "No restaurants found", ha='center', va='center', fontsize=12)
        ax.axis("off")

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
