"""
UI Components and styling for Twitter Sentiment Analysis
"""

import streamlit as st

def apply_custom_styles():
    """
    Apply custom CSS styles for premium UI
    """
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
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-5px);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 10px 0;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* ========== BUTTONS ========== */
        .stButton > button {
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
            background: linear-gradient(90deg, #2563eb, #7c3aed);
        }
        
        /* ========== SLIDER ========== */
        .stSlider > div > div > div {
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        }
        
        /* ========== HEADERS ========== */
        h1, h2, h3 {
            background: linear-gradient(90deg, #ffffff, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* ========== TWEET CARDS ========== */
        .tweet-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 20px;
            margin: 15px 0;
            border-left: 4px solid;
            transition: all 0.3s ease;
        }
        
        .tweet-card:hover {
            background: rgba(255, 255, 255, 0.06);
            transform: translateX(5px);
        }
        
        .positive-tweet {
            border-left-color: #10B981;
        }
        
        .negative-tweet {
            border-left-color: #EF4444;
        }
        
        .neutral-tweet {
            border-left-color: #6B7280;
        }
        
        .tweet-text {
            color: #e2e8f0;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        
        .tweet-meta {
            color: #94a3b8;
            font-size: 0.85rem;
            display: flex;
            justify-content: space-between;
        }
        
        /* ========== FOOTER ========== */
        .footer {
            text-align: center;
            padding: 30px 0;
            color: #94a3b8;
            font-size: 0.9rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 50px;
        }
        
        .footer a {
            color: #3b82f6;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer a:hover {
            color: #60a5fa;
            text-decoration: underline;
        }
        
        /* ========== CHECKBOX ========== */
        .stCheckbox > label {
            color: #cbd5e1;
            font-weight: 500;
        }
        
        /* ========== TEXT INPUT ========== */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 12px;
            padding: 12px 16px;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }
        
        /* ========== SUCCESS/WARNING/ERROR ========== */
        .stAlert {
            border-radius: 12px;
            border: none;
        }
        
        /* ========== SPINNER ========== */
        .stSpinner > div {
            border-color: #3b82f6 transparent transparent transparent;
        }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """
    Create application header with logo and title
    """
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 3rem; font-weight: 900; color: white;">𝕏</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: -10px;">Twitter</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h1 style="margin-bottom: 0;">Twitter Sentiment Analysis Dashboard</h1>
        <p style="color: #94a3b8; margin-top: 5px;">
            Real-time sentiment analysis with advanced AI and beautiful visualizations
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

def create_input_section():
    """
    Create input section for keyword search and tweet limit
    """
    st.markdown("### 🔍 Search Configuration")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        keyword = st.text_input(
            "Enter Keyword/Hashtag",
            placeholder="e.g., AI, ChatGPT, OpenAI",
            help="Enter a keyword or hashtag to search for tweets"
        )
    
    with col2:
        tweet_limit = st.slider(
            "Tweet Limit",
            min_value=2,
            max_value=20,
            value=10,
            help="Number of tweets to fetch and analyze"
        )
    
    with col3:
        remove_noise = st.checkbox(
            "Clean Tweets (remove emojis, hashtags, links)", 
            value=True,
            help="Clean tweet text before sentiment analysis"
        )
        st.write("")  # Spacer
        fetch_button = st.button("🚀 Fetch & Analyze Tweets", use_container_width=True)
    
    return keyword, tweet_limit, remove_noise, fetch_button

def create_metrics_display(metrics):
    """
    Display sentiment metrics in a visually appealing way
    
    Args:
        metrics (dict): Dictionary containing sentiment metrics
    """
    st.markdown("## 📊 Sentiment Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['total']}</div>
            <div class="metric-label">Total Tweets</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #10B981;">{metrics['positive']}</div>
            <div class="metric-label">Positive ({metrics['positive_percent']:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #EF4444;">{metrics['negative']}</div>
            <div class="metric-label">Negative ({metrics['negative_percent']:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #6B7280;">{metrics['neutral']}</div>
            <div class="metric-label">Neutral ({metrics['neutral_percent']:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)

def create_tweet_display(tweets):
    """
    Display individual tweets with sentiment coloring
    
    Args:
        tweets (list): List of processed tweet dictionaries
    """
    st.markdown("### 📝 Recent Tweets")
    
    for i, tweet in enumerate(tweets[:10]):  # Show first 10 tweets
        sentiment = tweet.get('sentiment', 'Neutral')
        
        # Determine CSS class based on sentiment
        sentiment_class = {
            'Positive': 'positive-tweet',
            'Negative': 'negative-tweet',
            'Neutral': 'neutral-tweet'
        }.get(sentiment, 'neutral-tweet')
        
        # Determine sentiment emoji
        sentiment_emoji = {
            'Positive': '✅',
            'Negative': '❌',
            'Neutral': '⚪'
        }.get(sentiment, '⚪')
        
        st.markdown(f"""
        <div class="tweet-card {sentiment_class}">
            <div class="tweet-text">
                {tweet.get('text', 'No text available')}
            </div>
            <div class="tweet-meta">
                <span>👤 {tweet.get('user', 'Unknown')}</span>
                <span>{sentiment_emoji} {sentiment}</span>
                <span>📅 {tweet.get('date', 'Unknown date')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_footer():
    """
    Create professional footer
    """
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>
            <strong>Twitter Sentiment Analysis Dashboard</strong> | 
            Built with ❤️ using Streamlit, VADER, and Plotly |
            API: RapidAPI Twitter API
        </p>
        <p>
            © 2024 Sentiment Analysis Platform | 
            <a href="#" target="_blank">Privacy Policy</a> | 
            <a href="#" target="_blank">Terms of Service</a>
        </p>
        <p style="font-size: 0.8rem; color: #64748b; margin-top: 10px;">
            Note: This tool analyzes public tweets for sentiment. No personal data is stored.
        </p>
    </div>
    """, unsafe_allow_html=True)