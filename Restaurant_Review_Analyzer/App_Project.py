# App_Project.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Restaurant Review Analyzer",
    page_icon=":fork_and_knife:",
    layout="wide"
)

st.header("Restaurant Review Analyzer 🍽️")

# --- Styling ---
st.markdown("""
<style>
/* Input Boxes */
[data-testid="stTextInput"] > div > div > input,
[data-testid="stTextArea"] > div > textarea {
    color: #f8fafc !important;
    border-radius: 7px;
    border: 1.5px solid #4b5563;
    font-size: 1.09em;
}
[data-testid="stTextInput"] > div > div > input::placeholder,
[data-testid="stTextArea"] > div > textarea::placeholder {
    color: #9ca3af !important;
    opacity: 1 !important;
    font-style: italic;
}

/* Fonts and Background */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto:wght@400;500&display=swap');

.stApp {
    background: linear-gradient(120deg, #1a2233 0%, #232932 100%) !important;
    font-family: 'Roboto', Arial, sans-serif;
    color: #eaeaea !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #232932 95%, #23324a 100%) !important;
    color: #eaf0fa !important;
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
    box-shadow: 6px 0 32px #000a;
}
.sidebar-welcome {
    background: #212b3a;
    border-radius: 18px;
    border-left: 5px solid #3b4252;
    margin-bottom: 16px;
    padding: 16px 10px 12px 10px;
    box-shadow: 0 2px 8px #28334780;
    text-align: center;
}
.sidebar-welcome p {
    color: #bedafc !important;
    font-size: 1em;
}

/* Headings */
.stTitle, h1 {
    color: #64c1f7 !important;
    font-family: 'Montserrat', Arial, sans-serif;
}
h2, h3 {
    color: #caf0f8 !important;
    font-family: 'Montserrat', Arial, sans-serif;
}

/* Tables */
.stDataFrame, .stTable {
    background: #1e2633 !important;
    border-radius: 16px !important;
    color: #f3f3f3 !important;
    font-size: 1.07em !important;
    box-shadow: 0 2px 14px #1c2737bc;
}

/* Buttons */
.stButton>button {
    background-color: #64c1f7 !important;
    color: #232932 !important;
    border-radius: 8px !important;
    font-weight: 600;
    border: none !important;
}
.stButton>button:hover {
    background-color: #3997ea !important;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# --- Load Data ---
file_path = "Hyderabad_Unique_Restaurants_Cleaned.xlsx"
df = pd.read_excel(file_path)

# --- Add Budget Categories ---
def price_category(price):
    if price < 200:
        return "$"
    elif 200 <= price < 400:
        return "$$"
    else:
        return "$$$"

df["Price_Range"] = df["Avg_Price_Restaurant"].apply(price_category)

# --- Sentiment Analysis ---
def analyze_sentiment(text):
    blob = TextBlob(str(text))
    if blob.sentiment.polarity > 0.1:
        return "Positive"
    elif blob.sentiment.polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# --- Session for User Reviews ---
if "reviews" not in st.session_state:
    st.session_state["reviews"] = pd.DataFrame(columns=["Restaurant_Name", "Review_Text", "Sentiment", "User_Rating"])

# --- Sidebar ---
st.sidebar.image("logo.png", width=120)
st.sidebar.markdown("""
<div class='sidebar-welcome'>
    <p>Explore Hyderabad's best restaurants 🍽️</p>
</div>
""", unsafe_allow_html=True)

budget_choice = st.sidebar.selectbox("Select Budget", ["$", "$$", "$$$"], index=0)
min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.5, 0.1)
cuisine_options = ["All"] + sorted(df["Cuisine"].dropna().unique())
cuisine_choice = st.sidebar.selectbox("Cuisine", cuisine_options)
search_name = st.sidebar.text_input("Search by Restaurant Name", "")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🌟 Recommended", "📝 Reviews", "📊 Insights"])

# --- TAB 1: Recommendations ---
with tab1:
    st.subheader("✨ Recommended Restaurants")
    filtered_df = df[(df["Price_Range"] == budget_choice) & (df["Average_Rating"] >= min_rating)]
    if cuisine_choice != "All":
        filtered_df = filtered_df[filtered_df["Cuisine"] == cuisine_choice]
    if search_name:
        filtered_df = filtered_df[filtered_df["Restaurant_Name"].str.contains(search_name, case=False, na=False)]

    if not filtered_df.empty:
        st.dataframe(filtered_df[["Restaurant_Name", "Cuisine", "Avg_Price_Restaurant", "Average_Rating", "Restaurant_Popularity"]])
    else:
        st.warning("No restaurants found matching your filters.")

# --- TAB 2: User Reviews ---
with tab2:
    st.subheader("📝 Add Your Review")
    with st.form("review_form"):
        restaurant_name = st.text_input("Restaurant Name")
        review_text = st.text_area("Your Review")
        user_rating = st.slider("Your Rating (1-5)", 1.0, 5.0, 3.0, 0.5)
        submit = st.form_submit_button("Submit Review")

    if submit:
        if restaurant_name.strip() and review_text.strip():
            sentiment = analyze_sentiment(review_text)
            new_review = pd.DataFrame({
                "Restaurant_Name": [restaurant_name],
                "Review_Text": [review_text],
                "Sentiment": [sentiment],
                "User_Rating": [user_rating]
            })
            st.session_state["reviews"] = pd.concat([st.session_state["reviews"], new_review], ignore_index=True)
            st.success(f"✅ Review added for {restaurant_name} ({sentiment})")
        else:
            st.error("Please provide both restaurant name and review text.")

    if not st.session_state["reviews"].empty:
        st.subheader("📖 User Reviews")
        st.dataframe(st.session_state["reviews"])

# --- TAB 3: Visual Insights ---
with tab3:
    st.subheader("📊 Visual Insights")

    col1, col2 = st.columns(2)

    # --- Price Distribution ---
    with col1:
        st.markdown("**Distribution of Average Prices**")
        fig, ax = plt.subplots()
        sns.histplot(df["Avg_Price_Restaurant"], bins=15, kde=True, color="skyblue", ax=ax)
        ax.set_xlabel("Average Price")
        st.pyplot(fig)

    # --- Ratings Distribution (Now combines both main df + user reviews) ---
    with col2:
        st.markdown("**Distribution of Ratings**")
        combined_ratings = pd.concat([
            df[["Restaurant_Name", "Average_Rating"]].rename(columns={"Average_Rating": "Rating"}),
            st.session_state["reviews"][["Restaurant_Name", "User_Rating"]].rename(columns={"User_Rating": "Rating"})
        ], ignore_index=True)

        if search_name:
            combined_ratings = combined_ratings[combined_ratings["Restaurant_Name"].str.contains(search_name, case=False, na=False)]

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.stripplot(x="Restaurant_Name", y="Rating", data=combined_ratings, jitter=True, palette="viridis", ax=ax)
        ax.set_title("Different Ratings per Restaurant")
        ax.set_xlabel("Restaurant")
        ax.set_ylabel("Rating")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    # --- Additional Visuals ---
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Most Popular Cuisines**")
        top_cuisines = df["Cuisine"].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=top_cuisines.values, y=top_cuisines.index, palette="coolwarm", ax=ax)
        ax.set_xlabel("Number of Restaurants")
        st.pyplot(fig)

    with col4:
        st.markdown("**Restaurant Popularity**")
        fig, ax = plt.subplots()
        sns.histplot(df["Restaurant_Popularity"], bins=15, kde=True, color="orange", ax=ax)
        ax.set_xlabel("Popularity Score")
        st.pyplot(fig)

st.markdown("---")
