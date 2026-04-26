"""
Main application file for Twitter Sentiment Analysis Dashboard
"""

import streamlit as st
import pandas as pd

# Import modules
# API key will be loaded from Streamlit secrets
API_KEY = "68ed5d9870msh56c48d238ea984bp1aba51jsn0c4437f4859b"  # Default fallback
from ui_components import apply_custom_styles, create_header, create_input_section, create_metrics_display, create_tweet_display, create_footer
from twitter_api import fetch_tweets, process_tweets
from visualizations import create_sentiment_bar_chart, create_sentiment_pie_chart, create_sentiment_donut_chart, create_sentiment_timeline, create_metrics_display as create_viz_metrics
from utils import create_dataframe, validate_input

# Page configuration
st.set_page_config(
    page_title="Twitter Sentiment Analysis",
    page_icon="𝕏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styles
apply_custom_styles()

# Security fix: Override API key from secrets if available
try:
    API_KEY = st.secrets["RAPIDAPI_KEY"]
except:
    pass  # Use the default from config.py

# Create header
create_header()

# Create input section
keyword, tweet_limit, remove_noise, fetch_button = create_input_section()

# Dashboard section
if fetch_button:
    # Validate input
    is_valid, error_message = validate_input(keyword, tweet_limit)
    
    if not is_valid:
        st.warning(f"⚠️ {error_message}")
    else:
        try:
            # Fetch tweets from API
            raw_tweets = fetch_tweets(keyword, tweet_limit, API_KEY)
            
            if not raw_tweets:
                st.error("No tweets found for this keyword. Try a different one.")
            else:
                # Process tweets with sentiment analysis
                tweets = process_tweets(raw_tweets, clean=remove_noise)
                
                # Create DataFrame
                df = create_dataframe(tweets)
                
                # Display success message
                st.success(f"✅ Successfully fetched and analyzed {len(tweets)} tweets!")
                
                # Calculate and display metrics
                metrics = create_viz_metrics(df)
                create_metrics_display(metrics)
                
                # Create visualizations
                st.markdown("## 📈 Visualizations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Bar chart
                    bar_chart = create_sentiment_bar_chart(df)
                    st.plotly_chart(bar_chart, use_container_width=True)
                    
                    # Pie chart
                    pie_chart = create_sentiment_pie_chart(df)
                    st.plotly_chart(pie_chart, use_container_width=True)
                
                with col2:
                    # Donut chart
                    donut_chart = create_sentiment_donut_chart(df)
                    st.plotly_chart(donut_chart, use_container_width=True)
                    
                    # Timeline chart
                    timeline_chart = create_sentiment_timeline(df)
                    st.plotly_chart(timeline_chart, use_container_width=True)
                
                # Display individual tweets
                create_tweet_display(tweets)
                
                # Export options
                st.markdown("## 📤 Export Results")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📥 Download as CSV", use_container_width=True):
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Click to download CSV",
                            data=csv,
                            file_name=f"sentiment_analysis_{keyword}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                with col2:
                    if st.button("📥 Download as JSON", use_container_width=True):
                        json_data = df.to_json(orient='records', indent=2).encode('utf-8')
                        st.download_button(
                            label="Click to download JSON",
                            data=json_data,
                            file_name=f"sentiment_analysis_{keyword}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                
                with col3:
                    if st.button("🔄 Reset Analysis", use_container_width=True):
                        st.rerun()
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your internet connection and try again.")

# Create footer
create_footer()

# Sidebar with information
with st.sidebar:
    st.markdown("## ℹ️ About")
    st.markdown("""
    This dashboard analyzes Twitter sentiment in real-time using:
    
    - **VADER Sentiment Analysis**: Advanced NLP model
    - **Keyword Boosting**: Custom sentiment enhancement
    - **Real-time API**: Latest tweets from Twitter
    - **Interactive Visualizations**: Multiple chart types
    
    ### How to use:
    1. Enter a keyword or hashtag
    2. Adjust tweet limit (2-20)
    3. Toggle tweet cleaning if needed
    4. Click "Fetch & Analyze Tweets"
    
    ### Features:
    - ✅ Real-time sentiment analysis
    - ✅ Multiple visualization types
    - ✅ Tweet cleaning options
    - ✅ Export results
    - ✅ Professional UI design
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔧 Technical Details")
    st.markdown("""
    - **Framework**: Streamlit
    - **Sentiment Engine**: VADER + Custom boosting
    - **Visualization**: Plotly
    - **API**: RapidAPI Twitter API
    - **UI**: Glassmorphism design
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Sentiment Scale")
    st.markdown("""
    - **Positive** (> 0.05): Green ✅
    - **Neutral** (-0.05 to 0.05): Gray ⚪  
    - **Negative** (< -0.05): Red ❌
    """)