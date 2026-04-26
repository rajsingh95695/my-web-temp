"""
Twitter API module for fetching tweets with pagination
"""

import requests
import streamlit as st
from config import TWITTER_API_URL

def fetch_tweets_with_pagination(keyword, tweet_limit, api_key, cursor=None):
    """
    Fetch tweets from Twitter API with pagination support
    
    Args:
        keyword (str): Search keyword
        tweet_limit (int): Maximum number of tweets to fetch
        cursor (str, optional): Cursor for pagination
        
    Returns:
        tuple: (list of tweets, next cursor)
    """
    # Build headers with provided API key
    headers = {
        "x-rapidapi-host": "twitter-api45.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }
    
    querystring = {
        "query": keyword,
        "search_type": "Latest"
    }
    
    if cursor:
        querystring["cursor"] = cursor
    
    try:
        response = requests.get(
            TWITTER_API_URL,
            headers=headers,
            params=querystring,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        tweets = data.get("timeline", [])
        next_cursor = data.get("cursor")
        
        return tweets, next_cursor
        
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return [], None
    except ValueError as e:
        st.error(f"JSON Parsing Error: {str(e)}")
        return [], None

def fetch_tweets(keyword, tweet_limit, api_key):
    """
    Fetch multiple pages of tweets until reaching the desired limit
    
    Args:
        keyword (str): Search keyword
        tweet_limit (int): Desired number of tweets
        
    Returns:
        list: List of tweet dictionaries
    """
    all_tweets = []
    cursor = None
    
    # Create a progress placeholder
    progress_placeholder = st.empty()
    
    with st.spinner("🔍 Fetching tweets from Twitter API..."):
        while len(all_tweets) < tweet_limit:
            # Update progress message
            progress_placeholder.info(f"📊 Fetched {len(all_tweets)}/{tweet_limit} tweets...")
            
            # Fetch next page
            new_tweets, cursor = fetch_tweets_with_pagination(keyword, tweet_limit, api_key, cursor)
            
            if not new_tweets:
                break
            
            # Process tweets
            for item in new_tweets:
                tweet_data = {
                    "text": item.get("text", ""),
                    "user": item.get("screen_name", "Unknown"),
                    "date": item.get("created_at", ""),
                    "retweets": item.get("retweet_count", 0),
                    "likes": item.get("favorite_count", 0)
                }
                all_tweets.append(tweet_data)
            
            # Break if no more tweets
            if not cursor:
                break
    
    # Clear progress placeholder
    progress_placeholder.empty()
    
    # Limit to requested number
    return all_tweets[:tweet_limit]

def process_tweets(tweets, clean=True):
    """
    Process raw tweets by adding sentiment analysis
    
    Args:
        tweets (list): List of raw tweet dictionaries
        clean (bool): Whether to clean tweets before sentiment analysis
        
    Returns:
        list: Processed tweets with sentiment analysis
    """
    from sentiment_analyzer import analyze_sentiment, get_sentiment_score
    
    processed_tweets = []
    
    for tweet in tweets:
        text = tweet.get("text", "")
        
        # Analyze sentiment
        sentiment = analyze_sentiment(text, clean=clean)
        
        # Calculate sentiment score with same cleaning preference
        if clean:
            from sentiment_analyzer import clean_tweet
            clean_text = clean_tweet(text)
            sentiment_score = get_sentiment_score(clean_text, clean=False)
        else:
            sentiment_score = get_sentiment_score(text, clean=False)
        
        processed_tweet = {
            "text": text,
            "user": tweet.get("user", "Unknown"),
            "date": tweet.get("date", ""),
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "retweets": tweet.get("retweets", 0),
            "likes": tweet.get("likes", 0)
        }
        
        processed_tweets.append(processed_tweet)
    
    return processed_tweets