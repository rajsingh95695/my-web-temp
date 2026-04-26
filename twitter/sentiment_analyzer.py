"""
Sentiment analysis module with VADER and keyword boosting
"""

import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import POSITIVE_WORDS, NEGATIVE_WORDS, POSITIVE_THRESHOLD, NEGATIVE_THRESHOLD

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def clean_tweet(text):
    """
    Clean tweet text by removing URLs, mentions, hashtags, emojis, and extra spaces
    
    Args:
        text (str): Raw tweet text
        
    Returns:
        str: Cleaned tweet text
    """
    if not text:
        return ""
    
    text = re.sub(r"http\S+", "", text)        # Remove URLs
    text = re.sub(r"@\w+", "", text)           # Remove mentions
    text = re.sub(r"#\w+", "", text)           # Remove hashtags
    text = re.sub(r"[^\w\s]", "", text)        # Remove emojis & symbols
    text = " ".join(text.split())              # Remove extra spaces
    return text

def analyze_sentiment(text, clean=True):
    """
    Analyze sentiment with VADER and keyword boosting
    
    Args:
        text (str): Text to analyze
        clean (bool): Whether to clean the text before analysis
        
    Returns:
        str: Sentiment label ("Positive", "Negative", or "Neutral")
    """
    if not text:
        return "Neutral"
    
    # Clean tweet text if requested
    if clean:
        text = clean_tweet(text)
    
    # Get base sentiment score from VADER
    score = analyzer.polarity_scores(text)["compound"]
    text_lower = text.lower()
    
    # Boost for positive words
    for word in POSITIVE_WORDS:
        if word in text_lower:
            score += 0.1
    
    # Boost for negative words
    for word in NEGATIVE_WORDS:
        if word in text_lower:
            score -= 0.1
    
    # Clamp score between -1 and 1
    score = max(-1.0, min(1.0, score))
    
    # Determine sentiment label
    if score > POSITIVE_THRESHOLD:
        return "Positive"
    elif score < NEGATIVE_THRESHOLD:
        return "Negative"
    else:
        return "Neutral"

def get_sentiment_score(text, clean=True):
    """
    Get raw sentiment score (without keyword boosting for visualization)
    
    Args:
        text (str): Text to analyze
        clean (bool): Whether to clean the text before analysis
        
    Returns:
        float: Sentiment score between -1 and 1
    """
    if not text:
        return 0.0
    
    if clean:
        text = clean_tweet(text)
    
    return analyzer.polarity_scores(text)["compound"]

def analyze_tweet_batch(tweets, clean=True):
    """
    Analyze sentiment for a batch of tweets
    
    Args:
        tweets (list): List of tweet dictionaries
        clean (bool): Whether to clean tweets before analysis
        
    Returns:
        list: List of analyzed tweet dictionaries with sentiment added
    """
    analyzed_tweets = []
    
    for tweet in tweets:
        if isinstance(tweet, dict):
            text = tweet.get("text", "")
        else:
            text = str(tweet)
        
        sentiment = analyze_sentiment(text, clean=clean)
        sentiment_score = get_sentiment_score(text, clean=clean)
        
        analyzed_tweet = {
            "text": text,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score
        }
        
        # Preserve other fields if present
        if isinstance(tweet, dict):
            analyzed_tweet.update({k: v for k, v in tweet.items() if k not in analyzed_tweet})
        
        analyzed_tweets.append(analyzed_tweet)
    
    return analyzed_tweets