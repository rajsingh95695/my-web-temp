"""
Utility functions for Twitter Sentiment Analysis
"""

import pandas as pd
from datetime import datetime

def format_date(date_string):
    """
    Format date string to readable format
    
    Args:
        date_string (str): Raw date string
        
    Returns:
        str: Formatted date string
    """
    if not date_string:
        return "Unknown date"
    
    try:
        # Try to parse various date formats
        if isinstance(date_string, str):
            # Remove timezone info if present
            date_string = date_string.split('+')[0].split('Z')[0].strip()
            
            # Try different date formats
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%a %b %d %H:%M:%S %Y']:
                try:
                    dt = datetime.strptime(date_string, fmt)
                    return dt.strftime('%b %d, %Y %I:%M %p')
                except ValueError:
                    continue
        
        return str(date_string)
    except:
        return str(date_string)

def create_dataframe(tweets):
    """
    Create pandas DataFrame from tweet list
    
    Args:
        tweets (list): List of tweet dictionaries
        
    Returns:
        pd.DataFrame: DataFrame with tweet data
    """
    if not tweets:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(tweets)
    
    # Format dates if present
    if 'date' in df.columns:
        df['formatted_date'] = df['date'].apply(format_date)
    
    return df

def validate_input(keyword, tweet_limit):
    """
    Validate user input
    
    Args:
        keyword (str): Search keyword
        tweet_limit (int): Number of tweets to fetch
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not keyword or not keyword.strip():
        return False, "Please enter a keyword to search"
    
    if len(keyword.strip()) < 2:
        return False, "Keyword must be at least 2 characters long"
    
    if tweet_limit < 2 or tweet_limit > 20:
        return False, "Tweet limit must be between 2 and 20"
    
    return True, ""

def calculate_sentiment_statistics(df):
    """
    Calculate detailed sentiment statistics
    
    Args:
        df (pd.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        dict: Dictionary with sentiment statistics
    """
    if df.empty:
        return {
            'total': 0,
            'sentiment_counts': {},
            'percentages': {},
            'average_score': 0,
            'sentiment_distribution': {}
        }
    
    total = len(df)
    
    # Count sentiments
    sentiment_counts = df['sentiment'].value_counts().to_dict()
    
    # Calculate percentages
    percentages = {}
    for sentiment, count in sentiment_counts.items():
        percentages[sentiment] = (count / total) * 100
    
    # Calculate average sentiment score
    average_score = df['sentiment_score'].mean() if 'sentiment_score' in df.columns else 0
    
    # Get sentiment distribution
    sentiment_distribution = {
        'positive_words': [],
        'negative_words': [],
        'common_words': []
    }
    
    return {
        'total': total,
        'sentiment_counts': sentiment_counts,
        'percentages': percentages,
        'average_score': average_score,
        'sentiment_distribution': sentiment_distribution
    }

def export_results(df, format='csv'):
    """
    Export analysis results to different formats
    
    Args:
        df (pd.DataFrame): DataFrame with analysis results
        format (str): Export format ('csv', 'json', 'excel')
        
    Returns:
        bytes: Exported data
    """
    if df.empty:
        return None
    
    if format == 'csv':
        return df.to_csv(index=False).encode('utf-8')
    elif format == 'json':
        return df.to_json(orient='records', indent=2).encode('utf-8')
    elif format == 'excel':
        # Note: Would need openpyxl or xlsxwriter for Excel export
        return None
    else:
        return None

def get_sentiment_color(sentiment):
    """
    Get color for sentiment
    
    Args:
        sentiment (str): Sentiment label
        
    Returns:
        str: Hex color code
    """
    color_map = {
        'Positive': '#10B981',  # Green
        'Negative': '#EF4444',  # Red
        'Neutral': '#6B7280'    # Gray
    }
    
    return color_map.get(sentiment, '#6B7280')

def get_sentiment_emoji(sentiment):
    """
    Get emoji for sentiment
    
    Args:
        sentiment (str): Sentiment label
        
    Returns:
        str: Emoji
    """
    emoji_map = {
        'Positive': '✅',
        'Negative': '❌',
        'Neutral': '⚪'
    }
    
    return emoji_map.get(sentiment, '⚪')