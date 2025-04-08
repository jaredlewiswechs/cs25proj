import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.data.path.append('/Users/jaredlewis/Desktop/Harvard CS50/senti.py')
nltk.download('vader_lexicon', download_dir='/Users/jaredlewis/Desktop/Harvard CS50/senti.py')

# Download VADER lexicon (only needed once)


st.title("News Topic Sentiment Analysis")



# --- Sidebar for User Inputs ---
st.sidebar.header("Configuration")
topic = st.sidebar.text_input("Enter a topic (e.g., climate change, technology)", "technology")
start_date = st.sidebar.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=7))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# Your NewsAPI key (provided)
news_api_key = "558f0188bf1641bb8bf5aba55c6f1f79"

if st.sidebar.button("Analyze"):
    st.subheader(f"News Headlines Sentiment for Topic: {topic}")

    # Build the NewsAPI URL with the topic query and date range.
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={topic}&"
        "sortBy=publishedAt&"
        f"from={start_date}&"
        f"to={end_date}&"
        "language=en&"
        f"apiKey={news_api_key}"
    )

    response = requests.get(url)

    if response.status_code == 200:
        news_json = response.json()
        articles = news_json.get("articles", [])

        if not articles:
            st.warning("No news articles found for your query and date range.")
        else:
            headlines = []
            sentiments = []
            dates = []

            # Initialize the VADER sentiment analyzer
            sia = SentimentIntensityAnalyzer()

            # Process each article to extract headline and compute sentiment
            for article in articles:
                headline = article.get("title", "")
                published_at = article.get("publishedAt", "")[:10]  # Extract date portion (YYYY-MM-DD)
                # Compute the compound sentiment score from VADER
                score = sia.polarity_scores(headline)['compound']
                headlines.append(headline)
                sentiments.append(score)
                dates.append(published_at)

            # Create a DataFrame for display and further analysis
            news_df = pd.DataFrame({
                "Date": dates,
                "Headline": headlines,
                "Sentiment": sentiments
            })
            st.write("### News Articles and Sentiment Scores", news_df)

            # Plot a histogram of the sentiment scores
            fig, ax = plt.subplots()
            ax.hist(news_df["Sentiment"], bins=20, color="blue", edgecolor="black")
            ax.set_title("Distribution of News Headline Sentiments")
            ax.set_xlabel("Sentiment Score (Compound)")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

            # Aggregate sentiment by date to see trend over time
            sentiment_by_date = news_df.groupby("Date")["Sentiment"].mean().reset_index()
            sentiment_by_date["Date"] = pd.to_datetime(sentiment_by_date["Date"])
            sentiment_by_date = sentiment_by_date.sort_values("Date")
            st.write("### Average Sentiment by Date")
            st.line_chart(sentiment_by_date.set_index("Date"))
    else:
        st.error(f"Error fetching news data: {response.text}")