"""
Visualization module for creating charts and graphs
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import COLORS

def create_sentiment_bar_chart(df):
    """
    Create bar chart showing sentiment distribution
    
    Args:
        df (pd.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    sentiment_counts = df['sentiment'].value_counts()
    
    # Define colors for each sentiment
    color_map = {
        'Positive': COLORS['positive'],
        'Negative': COLORS['negative'], 
        'Neutral': COLORS['neutral']
    }
    
    colors = [color_map.get(sent, COLORS['neutral']) for sent in sentiment_counts.index]
    
    fig = go.Figure(data=[
        go.Bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            marker_color=colors,
            text=sentiment_counts.values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='📊 Sentiment Distribution',
        xaxis_title='Sentiment',
        yaxis_title='Number of Tweets',
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    return fig

def create_sentiment_pie_chart(df):
    """
    Create pie chart showing sentiment percentages
    
    Args:
        df (pd.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    sentiment_counts = df['sentiment'].value_counts()
    
    # Define colors for each sentiment
    color_map = {
        'Positive': COLORS['positive'],
        'Negative': COLORS['negative'],
        'Neutral': COLORS['neutral']
    }
    
    colors = [color_map.get(sent, COLORS['neutral']) for sent in sentiment_counts.index]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.4,
            marker_colors=colors,
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='🥧 Sentiment Pie Chart',
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        showlegend=True
    )
    
    return fig

def create_sentiment_donut_chart(df):
    """
    Create donut chart showing sentiment percentages
    
    Args:
        df (pd.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        plotly.graph_objects.Figure: Donut chart figure
    """
    sentiment_counts = df['sentiment'].value_counts()
    
    # Define colors for each sentiment
    color_map = {
        'Positive': COLORS['positive'],
        'Negative': COLORS['negative'],
        'Neutral': COLORS['neutral']
    }
    
    colors = [color_map.get(sent, COLORS['neutral']) for sent in sentiment_counts.index]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.6,
            marker_colors=colors,
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='🍩 Sentiment Donut Chart',
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        showlegend=True
    )
    
    return fig

def create_sentiment_timeline(df):
    """
    Create line chart showing sentiment over time
    
    Args:
        df (pd.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        plotly.graph_objects.Figure: Line chart figure
    """
    if 'date' not in df.columns or df['date'].isnull().all():
        # Create dummy timeline if no dates available
        df = df.copy()
        df['order'] = range(len(df))
        
        fig = px.line(
            df, 
            x='order', 
            y='sentiment_score',
            color='sentiment',
            color_discrete_map={
                'Positive': COLORS['positive'],
                'Negative': COLORS['negative'],
                'Neutral': COLORS['neutral']
            },
            title='📈 Sentiment Timeline (by tweet order)',
            labels={'order': 'Tweet Order', 'sentiment_score': 'Sentiment Score'}
        )
    else:
        # Try to parse dates
        try:
            df['datetime'] = pd.to_datetime(df['date'])
            df = df.sort_values('datetime')
            
            fig = px.line(
                df, 
                x='datetime', 
                y='sentiment_score',
                color='sentiment',
                color_discrete_map={
                    'Positive': COLORS['positive'],
                    'Negative': COLORS['negative'],
                    'Neutral': COLORS['neutral']
                },
                title='📈 Sentiment Timeline',
                labels={'datetime': 'Time', 'sentiment_score': 'Sentiment Score'}
            )
        except:
            # Fallback to dummy timeline
            df = df.copy()
            df['order'] = range(len(df))
            
            fig = px.line(
                df, 
                x='order', 
                y='sentiment_score',
                color='sentiment',
                color_discrete_map={
                    'Positive': COLORS['positive'],
                    'Negative': COLORS['negative'],
                    'Neutral': COLORS['neutral']
                },
                title='📈 Sentiment Timeline (by tweet order)',
                labels={'order': 'Tweet Order', 'sentiment_score': 'Sentiment Score'}
            )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400,
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    return fig

def create_metrics_display(df):
    """
    Calculate and return sentiment metrics
    
    Args:
        df (pd.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        dict: Dictionary containing sentiment metrics
    """
    total_tweets = len(df)
    
    if total_tweets == 0:
        return {
            'total': 0,
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'positive_percent': 0,
            'negative_percent': 0,
            'neutral_percent': 0,
            'avg_sentiment': 0
        }
    
    positive_tweets = len(df[df['sentiment'] == 'Positive'])
    negative_tweets = len(df[df['sentiment'] == 'Negative'])
    neutral_tweets = len(df[df['sentiment'] == 'Neutral'])
    
    positive_percent = (positive_tweets / total_tweets) * 100
    negative_percent = (negative_tweets / total_tweets) * 100
    neutral_percent = (neutral_tweets / total_tweets) * 100
    
    avg_sentiment = df['sentiment_score'].mean() if 'sentiment_score' in df.columns else 0
    
    return {
        'total': total_tweets,
        'positive': positive_tweets,
        'negative': negative_tweets,
        'neutral': neutral_tweets,
        'positive_percent': positive_percent,
        'negative_percent': negative_percent,
        'neutral_percent': neutral_percent,
        'avg_sentiment': avg_sentiment
    }