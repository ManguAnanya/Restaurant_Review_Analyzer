import pandas as pd
from textblob import TextBlob

# --- 1. Load Data from Excel ---
file_path = "D:/College/Sem-03/DAV/Programs/Restuarant_Review_Analyzer/Hyderabad_Unique_Restaurants_Cleaned.xlsx"
df = pd.read_excel(file_path)

# --- 2. Map Cost to Categories ---
def price_category(price):
    if price < 200:
        return "$"
    elif 200 <= price < 400:
        return "$$"
    else:
        return "$$$"

df["price_range"] = df["Avg_Price_Restaurant"].apply(price_category)

# Mapping symbols to numeric levels
price_map = {"$": 1, "$$": 2, "$$$": 3}
df["price_numeric"] = df["price_range"].map(price_map)

# --- 3. Sentiment Analysis ---
def analyze_sentiment(text):
    blob = TextBlob(str(text))
    return blob.sentiment.polarity

# For now: dummy reviews (can be replaced with actual user reviews)
reviews = pd.DataFrame({
    "restaurant": df["Restaurant_Name"],
    "review_text": ["Good food and ambience"] * len(df)
})
reviews["polarity"] = reviews["review_text"].apply(analyze_sentiment)

# Merge back into df: average polarity per restaurant
avg_sentiment = reviews.groupby("restaurant")["polarity"].mean().reset_index()
avg_sentiment.rename(columns={"polarity": "average_polarity"}, inplace=True)
df = df.merge(avg_sentiment, left_on="Restaurant_Name", right_on="restaurant", how="left")

# --- 4. Recommend Restaurants ---
def recommend_restaurants(customer_budget_symbol, top_n=5):
    if customer_budget_symbol not in price_map:
        print(f"Invalid budget symbol: {customer_budget_symbol}. Please use '$', '$$', or '$$$'.")
        return

    customer_budget_numeric = price_map[customer_budget_symbol]

    affordable_restaurants = df[df['price_numeric'] <= customer_budget_numeric].copy()

    if affordable_restaurants.empty:
        print(f"\nNo restaurants found within your budget ({customer_budget_symbol}).")
        return

    recommended_restaurants = affordable_restaurants.sort_values(
        by='average_polarity', ascending=False
    ).head(top_n)

    print(f"\n--- Top {top_n} Recommendations for Budget: {customer_budget_symbol} ---")
    for i, row in recommended_restaurants.iterrows():
        print(f"\nRestaurant: {row['Restaurant_Name']}")
        print(f"Price Range: {row['price_range']}")
        print(f"Average Sentiment Score: {row['average_polarity']:.2f}")
        print("-" * 50)

# --- 5. Add Reviews ---
def add_review(restaurant, review_text):
    global reviews, df
    sentiment = analyze_sentiment(review_text)
    new_row = pd.DataFrame({
        "restaurant": [restaurant],
        "review_text": [review_text],
        "polarity": [sentiment]
    })
    reviews = pd.concat([reviews, new_row], ignore_index=True)

    # Update df average polarity
    avg_sentiment = reviews.groupby("restaurant")["polarity"].mean().reset_index()
    avg_sentiment.rename(columns={"polarity": "average_polarity"}, inplace=True)
    df.update(avg_sentiment.set_index("restaurant"), overwrite=True)

    print(f"✅ Review added for {restaurant} (score {sentiment:.2f})")

# --- Run Program ---
if __name__ == "__main__":
    print("Welcome to the Hyderabad Restaurant Recommender 🍽️")
    while True:
        choice = input("\nEnter budget ($/$$/$$$) or 'q' to quit: ").strip()
        if choice.lower() == "q":
            break
        recommend_restaurants(choice, top_n=5)

        add_choice = input("Would you like to add a review? (y/n): ").strip().lower()
        if add_choice == "y":
            rest = input("Enter restaurant name: ")
            review = input("Enter your review: ")
            add_review(rest, review)
