import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime
import re

# Security fix: API key from secrets
API_KEY = st.secrets["RAPIDAPI_KEY"]

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Keyword boosting lists
POSITIVE_WORDS = ["good", "great", "excellent", "amazing", "awesome", "fantastic",
                  "love", "best", "super", "nice", "brilliant", "happy", "win", "success"]
NEGATIVE_WORDS = ["bad", "worst", "terrible", "awful", "hate", "poor", "sad",
                  "loss", "fail", "angry", "disappointed", "useless"]

# Tweet cleaning function
def clean_tweet(text):
    """Clean tweet text by removing URLs, mentions, hashtags, emojis, and extra spaces"""
    text = re.sub(r"http\S+", "", text)        # Remove URLs
    text = re.sub(r"@\w+", "", text)           # Remove mentions
    text = re.sub(r"#\w+", "", text)           # Remove hashtags
    text = re.sub(r"[^\w\s]", "", text)        # Remove emojis & symbols
    text = " ".join(text.split())              # Remove extra spaces
    return text

# Enhanced sentiment analysis with keyword boosting
def analyze_sentiment(text, clean=True):
    """Analyze sentiment with VADER and keyword boosting"""
    if not text:
        return "Neutral"
    
    # Clean tweet text if requested
    if clean:
        text = clean_tweet(text)
    
    score = analyzer.polarity_scores(text)["compound"]
    text_lower = text.lower()
    
    # Boost for positive words
    for w in POSITIVE_WORDS:
        if w in text_lower:
            score += 0.1
    
    # Boost for negative words
    for w in NEGATIVE_WORDS:
        if w in text_lower:
            score -= 0.1
    
    # Clamp score between -1 and 1
    score = max(-1.0, min(1.0, score))
    
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

# Premium UI Styling with Twitter X Theme
st.markdown("""
<style>
    /* ========== BACKGROUND ========== */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        background-attachment: fixed;
        font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* ========== GLASSMORPHISM CARDS ========== */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin-bottom: 25px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* ========== METRIC CARDS ========== */
    .metric-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        border-radius: 18px;
        padding: 25px 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: scale(1.08);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
    }
    
    /* ========== TWEET CARDS ========== */
    .tweet-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(8px);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 20px;
        border-left: 6px solid;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .tweet-card:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(8px) scale(1.01);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
    }
    
    .positive-tweet {
        border-left-color: #10b981;
    }
    
    .negative-tweet {
        border-left-color: #ef4444;
    }
    
    .neutral-tweet {
        border-left-color: #94a3b8;
    }
    
    /* ========== HEADERS ========== */
    .main-header {
        font-size: 3.2rem;
        font-weight: 900;
        color: white;
        text-align: center;
        margin-bottom: 15px;
        letter-spacing: -0.5px;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .main-header .x-logo {
        color: white;
        font-weight: 900;
        display: inline-block;
        margin-right: 10px;
    }
    
    .sub-header {
        color: rgba(255, 255, 255, 0.75);
        text-align: center;
        margin-bottom: 50px;
        font-size: 1.3rem;
        font-weight: 400;
        letter-spacing: 0.3px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    /* ========== BUTTON ENHANCEMENT ========== */
    .stButton > button {
        background: linear-gradient(45deg, #3b82f6, #8b5cf6, #ec4899) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px 42px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        transition: all 0.4s ease !important;
        width: 100% !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3) !important;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.03) !important;
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(45deg, #2563eb, #7c3aed, #db2777) !important;
    }
    
    /* ========== INPUT BOX ========== */
    .stTextInput > div > div > input {
        border-radius: 14px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        padding: 16px 20px !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        background: rgba(255, 255, 255, 0.12) !important;
        outline: none !important;
    }
    
    /* ========== SLIDER ========== */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
    }
    
    .stSlider > div > div > div > div > div {
        background: white !important;
        border: 3px solid #3b82f6 !important;
    }
    
    /* ========== SECTION SPACING ========== */
    .main .block-container {
        padding-top: 40px;
        padding-bottom: 60px;
    }
    
    h1, h2, h3 {
        margin-top: 30px !important;
        margin-bottom: 20px !important;
    }
    
    /* ========== HIDE DEFAULT ELEMENTS ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #3b82f6, #8b5cf6);
        border-radius: 10px;
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .sub-header {
            font-size: 1.1rem;
        }
        .metric-card {
            padding: 20px 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Page config
st.set_page_config(
    page_title="Twitter Sentiment Dashboard",
    page_icon="𝕏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Main header with Twitter X logo
st.markdown('<h1 class="main-header"><span class="x-logo">𝕏</span> Twitter Sentiment Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Real-time sentiment analysis of Twitter data with advanced AI insights</p>', unsafe_allow_html=True)

# Main container
with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        keyword = st.text_input(
            "🔍 Enter keyword (e.g., Dhoni, IPL, AI, Bitcoin)",
            placeholder="Type your keyword here...",
            help="Enter any keyword to fetch real tweets from Twitter"
        )
    
    with col2:
        tweet_limit = st.slider(
            "📊 Tweet limit",
            min_value=2,
            max_value=20,
            value=20,
            help="Number of tweets to analyze"
        )
    
    with col3:
        remove_noise = st.checkbox("Clean Tweets (remove emojis, hashtags, links)", value=True)
        st.write("")  # Spacer
        fetch_button = st.button("🚀 Fetch & Analyze Tweets", use_container_width=True)

# Dashboard section
if fetch_button:
    if not keyword:
        st.warning("⚠️ Please enter a keyword to search")
    else:
        # API call with pagination to fetch more tweets
        url = "https://twitter-api45.p.rapidapi.com/search.php"
        headers = {
            "x-rapidapi-host": "twitter-api45.p.rapidapi.com",
            "x-rapidapi-key": API_KEY
        }
        
        try:
            all_tweets = []
            cursor = None
            
            # Create a progress placeholder
            progress_placeholder = st.empty()
            
            with st.spinner("🔍 Fetching tweets from Twitter API..."):
                while len(all_tweets) < tweet_limit:
                    # Update progress message
                    progress_placeholder.info(f"📊 Fetched {len(all_tweets)}/{tweet_limit} tweets...")
                    
                    # Build query with cursor if available
                    querystring = {
                        "query": keyword,
                        "search_type": "Latest"
                    }
                    if cursor:
                        querystring["cursor"] = cursor
                    
                    response = requests.get(url, headers=headers, params=querystring)
                    data = response.json()
                    
                    new_tweets = data.get("timeline", [])
                    
                    for item in new_tweets:
                        tweet_text = item.get("text", "")
                        sentiment = analyze_sentiment(tweet_text, clean=remove_noise)
                        
                        # Calculate sentiment score with same cleaning preference
                        if remove_noise:
                            clean_text = clean_tweet(tweet_text)
                            sentiment_score = analyzer.polarity_scores(clean_text)["compound"]
                        else:
                            sentiment_score = analyzer.polarity_scores(tweet_text)["compound"]
                        
                        all_tweets.append({
                            "text": tweet_text,
                            "user": item.get("screen_name", "Unknown"),
                            "date": item.get("created_at", ""),
                            "sentiment": sentiment,
                            "sentiment_score": sentiment_score
                        })
                    
                    # Update cursor for next page
                    cursor = data.get("cursor")
                    
                    # Break if no more tweets
                    if not cursor:
                        break
        
            # Clear progress placeholder
            progress_placeholder.empty()
            
            # Limit to requested number
            tweets = all_tweets[:tweet_limit]
            
            if not tweets:
                st.error("No tweets found for this keyword. Try a different one.")
            else:
                st.success(f"✅ Successfully fetched and analyzed {len(tweets)} tweets!")
                
                # Create DataFrame for analysis
                df = pd.DataFrame(tweets)
                    
                # Calculate metrics
                total_tweets = len(df)
                positive_tweets = len(df[df['sentiment'] == 'Positive'])
                negative_tweets = len(df[df['sentiment'] == 'Negative'])
                neutral_tweets = len(df[df['sentiment'] == 'Neutral'])
                
                positive_percent = (positive_tweets / total_tweets * 100) if total_tweets > 0 else 0
                negative_percent = (negative_tweets / total_tweets * 100) if total_tweets > 0 else 0
                neutral_percent = (neutral_tweets / total_tweets * 100) if total_tweets > 0 else 0
                
                # Metrics Dashboard
                st.markdown("## 📊 Sentiment Dashboard")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3 style="color: #4CAF50; font-size: 2.5rem;">{positive_tweets}</h3>
                        <p style="color: white; font-size: 1.1rem;">Positive</p>
                        <p style="color: rgba(255,255,255,0.7);">{positive_percent:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3 style="color: #F44336; font-size: 2.5rem;">{negative_tweets}</h3>
                        <p style="color: white; font-size: 1.1rem;">Negative</p>
                        <p style="color: rgba(255,255,255,0.7);">{negative_percent:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3 style="color: #9E9E9E; font-size: 2.5rem;">{neutral_tweets}</h3>
                        <p style="color: white; font-size: 1.1rem;">Neutral</p>
                        <p style="color: rgba(255,255,255,0.7);">{neutral_percent:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3 style="color: #2196F3; font-size: 2.5rem;">{total_tweets}</h3>
                        <p style="color: white; font-size: 1.1rem;">Total Tweets</p>
                        <p style="color: rgba(255,255,255,0.7);">Analyzed</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Charts Section
                st.markdown("## 📈 Visualization Dashboard")
                
                # Prepare data for charts
                sentiment_counts = df['sentiment'].value_counts()
                
                # 1. Bar Chart
                fig_bar = go.Figure(data=[
                    go.Bar(
                        x=sentiment_counts.index,
                        y=sentiment_counts.values,
                        marker_color=['#4CAF50', '#F44336', '#9E9E9E'],
                        text=sentiment_counts.values,
                        textposition='auto',
                    )
                ])
                fig_bar.update_layout(
                    title="Sentiment Distribution (Bar Chart)",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                
                # 2. Pie Chart
                fig_pie = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="Sentiment Distribution (Pie Chart)",
                    color=sentiment_counts.index,
                    color_discrete_map={'Positive':'#4CAF50', 'Negative':'#F44336', 'Neutral':'#9E9E9E'}
                )
                fig_pie.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                
                # 3. Donut Chart
                fig_donut = go.Figure(data=[go.Pie(
                    labels=sentiment_counts.index,
                    values=sentiment_counts.values,
                    hole=.4,
                    marker_colors=['#4CAF50', '#F44336', '#9E9E9E']
                )])
                fig_donut.update_layout(
                    title="Sentiment Distribution (Donut Chart)",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                
                # 4. Line Chart (sentiment score over time/index)
                df['index'] = range(len(df))
                fig_line = px.line(
                    df, 
                    x='index', 
                    y='sentiment_score',
                    title="Sentiment Score Trend Across Tweets",
                    markers=True
                )
                fig_line.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title="Tweet Index",
                    yaxis_title="Sentiment Score"
                )
                fig_line.add_hline(y=0.05, line_dash="dash", line_color="#4CAF50", annotation_text="Positive Threshold")
                fig_line.add_hline(y=-0.05, line_dash="dash", line_color="#F44336", annotation_text="Negative Threshold")
                
                # Display charts in columns
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig_bar, use_container_width=True)
                    st.plotly_chart(fig_donut, use_container_width=True)
                
                with col2:
                    st.plotly_chart(fig_pie, use_container_width=True)
                    st.plotly_chart(fig_line, use_container_width=True)
                
                # Tweets Display Section
                st.markdown("## 🐦 Analyzed Tweets")
                st.markdown(f"Showing {len(tweets)} tweets for keyword: **{keyword}**")
                
                for i, tweet in enumerate(tweets):
                    sentiment_class = f"{tweet['sentiment'].lower()}-tweet"
                    sentiment_color = {
                        "Positive": "#4CAF50",
                        "Negative": "#F44336",
                        "Neutral": "#9E9E9E"
                    }[tweet['sentiment']]
                    
                    st.markdown(f"""
                    <div class="tweet-card {sentiment_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong style="color: white;">@{tweet['user']}</strong>
                                <span style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-left: 10px;">{tweet['date']}</span>
                            </div>
                            <div style="background: {sentiment_color}; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">
                                {tweet['sentiment']}
                            </div>
                        </div>
                        <p style="color: white; margin-top: 15px; line-height: 1.5;">{tweet['text']}</p>
                        <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 10px;">
                            Score: {tweet['sentiment_score']:.3f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Export option
                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info("💡 **Insight**: The sentiment analysis uses VADER with keyword boosting for more accurate results.")
                with col2:
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"twitter_sentiment_{keyword}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        
        except Exception as e:
            st.error(f"Error fetching tweets: {str(e)}")
            st.info("Please check your API key or try again later.")

# Professional Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.5); padding: 15px; font-size: 0.9rem;">
    🚀 Advanced AI Sentiment Engine | Real-time Social Media Insights
</div>
""", unsafe_allow_html=True)