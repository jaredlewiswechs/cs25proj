import streamlit as st
import tweepy
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Twitter API credentials for v2 (you need to generate a bearer token in your developer portal)
bearer_token = "AAAAAAAAAAAAAAAAAAAAAMnC0QEAAAAAbMvEb06U4pXyQ%2Fb3KcWRD53QGUA%3D6NfQoAqjuLbKbcrAr4m9a8NS4FotdUMxcoPLyQDRvRJd7GVS3A"  # Replace with your actual bearer token
consumer_key = "YLznFZ9cE8znuLbONqsgKt3E9"
consumer_secret = "UBtohvvD4R9m010eatRoMTokGRBIi3KTGxHyChCbvhdrRTzXCa"
access_token = "1662144690785861633-nl1nt7g629iR8dCwHXHmG5WxQWP68A"
access_secret = "XRZufpKmdcpcZ0XL1aE2ToFVSQ5ZkZ2Wd6TPji6B86Plm"

# Create a Tweepy client for Twitter API v2
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_secret,
                       wait_on_rate_limit=True)

st.title("Tweet Sentiment Analysis")

# User inputs for search term and number of tweets
query = st.text_input("Enter a search term or hashtag:", "#rstats")
num_tweets = st.number_input("Number of tweets to fetch:", min_value=10, value=100, step=1)

if st.button("Analyze"):
    tweets_data = []
    try:
        # Use Tweepy Client to search recent tweets.
        # Note: The max_results parameter accepts a maximum of 100 per request.
        max_results = min(num_tweets, 100)
        tweets = client.search_recent_tweets(query=query,
                                             max_results=max_results,
                                             tweet_fields=["created_at", "text", "author_id"])
        if tweets.data is None:
            st.warning("No tweets found for your query.")
        else:
            for tweet in tweets.data:
                text = tweet.text
                analysis = TextBlob(text)
                sentiment_score = analysis.sentiment.polarity
                tweets_data.append({
                    "created_at": tweet.created_at,
                    "author_id": tweet.author_id,
                    "text": text,
                    "sentiment_score": sentiment_score
                })
            df = pd.DataFrame(tweets_data)
            st.write("### Fetched Tweets", df)

            # Plot a histogram of sentiment scores
            fig, ax = plt.subplots()
            ax.hist(df["sentiment_score"], bins=20, color="blue", edgecolor="black")
            ax.set_title("Distribution of Tweet Sentiment Scores")
            ax.set_xlabel("Sentiment Score (Polarity)")
            ax.set_ylabel("Number of Tweets")
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Error fetching tweets: {e}")