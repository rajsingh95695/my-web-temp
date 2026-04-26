"""
Configuration and constants for Twitter Sentiment Analysis
"""

# API Configuration
TWITTER_API_URL = "https://twitter-api45.p.rapidapi.com/search.php"

# Note: API_KEY will be set dynamically in main.py from Streamlit secrets
# TWITTER_API_HEADERS will be constructed dynamically

# Sentiment Analysis Configuration
POSITIVE_WORDS = [
    "good", "great", "excellent", "amazing", "awesome", "fantastic",
    "love", "best", "super", "nice", "brilliant", "happy", "win", "success"
]

NEGATIVE_WORDS = [
    "bad", "worst", "terrible", "awful", "hate", "poor", "sad",
    "loss", "fail", "angry", "disappointed", "useless"
]

# UI Configuration
DEFAULT_TWEET_LIMIT = 10
MIN_TWEET_LIMIT = 2
MAX_TWEET_LIMIT = 20

# Sentiment Thresholds
POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05

# Color Scheme
COLORS = {
    "positive": "#10B981",  # Green
    "negative": "#EF4444",  # Red
    "neutral": "#6B7280",   # Gray
    "background": "#0f172a",
    "card": "rgba(255, 255, 255, 0.05)",
    "border": "rgba(255, 255, 255, 0.1)"
}