"""Twitter API service for sentiment analysis platform"""

import requests
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class TwitterService:
    """Service for interacting with Twitter API"""
    
    def __init__(self, api_key: str, api_secret: str, bearer_token: Optional[str] = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.rate_limit_remaining = 450
        self.rate_limit_reset = None
        self.session = requests.Session()
        
        if bearer_token:
            self.session.headers.update({
                'Authorization': f'Bearer {bearer_token}'
            })
    
    def search_tweets(self, query: str, max_results: int = 100, 
                     start_time: Optional[str] = None,
                     end_time: Optional[str] = None) -> Dict[str, Any]:
        """Search for tweets using Twitter API v2"""
        
        endpoint = f"{self.base_url}/tweets/search/recent"
        params = {
            'query': query,
            'max_results': min(max_results, 100),  # API limit
            'tweet.fields': 'created_at,public_metrics,text,author_id',
            'user.fields': 'username,name',
            'expansions': 'author_id'
        }
        
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        
        try:
            self._check_rate_limit()
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            
            # Update rate limit info
            self._update_rate_limit(response.headers)
            
            data = response.json()
            return self._process_search_response(data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Twitter API request failed: {e}")
            raise
    
    def get_user_tweets(self, user_id: str, max_results: int = 100) -> Dict[str, Any]:
        """Get tweets from a specific user"""
        
        endpoint = f"{self.base_url}/users/{user_id}/tweets"
        params = {
            'max_results': min(max_results, 100),
            'tweet.fields': 'created_at,public_metrics,text',
            'exclude': 'retweets,replies'  # Only original tweets
        }
        
        try:
            self._check_rate_limit()
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            
            self._update_rate_limit(response.headers)
            data = response.json()
            return self._process_timeline_response(data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get user tweets: {e}")
            raise
    
    def stream_tweets(self, filter_rules: List[Dict[str, str]], 
                     timeout: int = 30) -> List[Dict[str, Any]]:
        """Stream tweets in real-time (simulated for demo)"""
        
        logger.info(f"Starting tweet stream with rules: {filter_rules}")
        
        # Simulate streaming by returning sample data
        # In production, this would connect to Twitter streaming API
        sample_tweets = [
            {
                'id': 'stream_1',
                'text': 'Real-time tweet about technology',
                'user_id': 'user_123',
                'created_at': datetime.utcnow().isoformat() + 'Z',
                'retweet_count': 5,
                'like_count': 20,
                'reply_count': 3
            },
            {
                'id': 'stream_2',
                'text': 'Another real-time update',
                'user_id': 'user_456',
                'created_at': datetime.utcnow().isoformat() + 'Z',
                'retweet_count': 2,
                'like_count': 10,
                'reply_count': 1
            }
        ]
        
        # Simulate delay for streaming
        time.sleep(1)
        
        return sample_tweets
    
    def get_tweet_metrics(self, tweet_id: str) -> Dict[str, Any]:
        """Get detailed metrics for a specific tweet"""
        
        endpoint = f"{self.base_url}/tweets/{tweet_id}"
        params = {
            'tweet.fields': 'public_metrics,created_at,text,author_id',
            'expansions': 'author_id'
        }
        
        try:
            self._check_rate_limit()
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            
            self._update_rate_limit(response.headers)
            data = response.json()
            
            if 'data' in data:
                tweet_data = data['data']
                return {
                    'id': tweet_data['id'],
                    'text': tweet_data.get('text', ''),
                    'created_at': tweet_data.get('created_at', ''),
                    'metrics': tweet_data.get('public_metrics', {}),
                    'author_id': tweet_data.get('author_id', '')
                }
            else:
                return {}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get tweet metrics: {e}")
            raise
    
    def _process_search_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process Twitter API search response"""
        
        tweets = []
        users = {}
        
        # Extract user information
        if 'includes' in response_data and 'users' in response_data['includes']:
            for user in response_data['includes']['users']:
                users[user['id']] = {
                    'username': user.get('username', ''),
                    'name': user.get('name', '')
                }
        
        # Process tweets
        if 'data' in response_data:
            for tweet in response_data['data']:
                author_info = users.get(tweet.get('author_id', ''), {})
                
                processed_tweet = {
                    'id': tweet['id'],
                    'text': tweet.get('text', ''),
                    'created_at': tweet.get('created_at', ''),
                    'author_id': tweet.get('author_id', ''),
                    'author_username': author_info.get('username', ''),
                    'author_name': author_info.get('name', ''),
                    'retweet_count': tweet.get('public_metrics', {}).get('retweet_count', 0),
                    'reply_count': tweet.get('public_metrics', {}).get('reply_count', 0),
                    'like_count': tweet.get('public_metrics', {}).get('like_count', 0),
                    'quote_count': tweet.get('public_metrics', {}).get('quote_count', 0)
                }
                tweets.append(processed_tweet)
        
        result = {
            'tweets': tweets,
            'count': len(tweets),
            'next_token': response_data.get('meta', {}).get('next_token'),
            'total_count': response_data.get('meta', {}).get('result_count', 0)
        }
        
        return result
    
    def _process_timeline_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user timeline response"""
        
        tweets = []
        
        if 'data' in response_data:
            for tweet in response_data['data']:
                processed_tweet = {
                    'id': tweet['id'],
                    'text': tweet.get('text', ''),
                    'created_at': tweet.get('created_at', ''),
                    'retweet_count': tweet.get('public_metrics', {}).get('retweet_count', 0),
                    'reply_count': tweet.get('public_metrics', {}).get('reply_count', 0),
                    'like_count': tweet.get('public_metrics', {}).get('like_count', 0),
                    'quote_count': tweet.get('public_metrics', {}).get('quote_count', 0)
                }
                tweets.append(processed_tweet)
        
        return {
            'tweets': tweets,
            'count': len(tweets),
            'next_token': response_data.get('meta', {}).get('next_token')
        }
    
    def _check_rate_limit(self) -> None:
        """Check and handle rate limits"""
        
        if self.rate_limit_remaining <= 10:
            if self.rate_limit_reset:
                reset_time = datetime.fromtimestamp(self.rate_limit_reset)
                wait_seconds = (reset_time - datetime.now()).total_seconds()
                
                if wait_seconds > 0:
                    logger.warning(f"Rate limit approaching. Waiting {wait_seconds:.0f} seconds.")
                    time.sleep(min(wait_seconds, 300))  # Max wait 5 minutes
    
    def _update_rate_limit(self, headers: Dict[str, str]) -> None:
        """Update rate limit information from response headers"""
        
        if 'x-rate-limit-remaining' in headers:
            self.rate_limit_remaining = int(headers['x-rate-limit-remaining'])
        
        if 'x-rate-limit-reset' in headers:
            self.rate_limit_reset = int(headers['x-rate-limit-reset'])
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get current rate limit information"""
        
        return {
            'remaining': self.rate_limit_remaining,
            'reset_timestamp': self.rate_limit_reset,
            'reset_time': datetime.fromtimestamp(self.rate_limit_reset).isoformat() 
                         if self.rate_limit_reset else None
        }

class MockTwitterService(TwitterService):
    """Mock Twitter service for testing and development"""
    
    def __init__(self):
        super().__init__(api_key='mock_key', api_secret='mock_secret')
        self.mock_tweets = self._generate_mock_tweets()
    
    def search_tweets(self, query: str, max_results: int = 100, **kwargs) -> Dict[str, Any]:
        """Mock search tweets"""
        
        logger.info(f"Mock search for: {query}, max_results: {max_results}")
        
        # Filter mock tweets by query (simplified)
        filtered_tweets = [
            tweet for tweet in self.mock_tweets 
            if query.lower() in tweet['text'].lower()
        ][:max_results]
        
        return {
            'tweets': filtered_tweets,
            'count': len(filtered_tweets),
            'next_token': 'mock_next_token',
            'total_count': len(filtered_tweets)
        }
    
    def _generate_mock_tweets(self) -> List[Dict[str, Any]]:
        """Generate mock tweet data"""
        
        mock_tweets = []
        base_time = datetime.utcnow()
        
        sentiments = ['positive', 'negative', 'neutral']
        topics = ['technology', 'sports', 'politics', 'entertainment', 'business']
        
        for i in range(1, 101):
            sentiment = sentiments[i % 3]
            topic = topics[i % 5]
            
            if sentiment == 'positive':
                text = f"Great news about {topic}! Really excited about the developments. #{topic}"
            elif sentiment == 'negative':
                text = f"Terrible situation with {topic}. Very disappointed. #{topic}"
            else:
                text = f"Update on {topic}. The situation is developing. #{topic}"
            
            tweet_time = base_time - timedelta(minutes=i*10)
            
            mock_tweets.append({
                'id': f'mock_tweet_{i}',
                'text': text,
                'created_at': tweet_time.isoformat() + 'Z',
                'author_id': f'user_{i % 20}',
                'author_username': f'user_{i % 20}',
                'author_name': f'User {i % 20}',
                'retweet_count': i % 100,
                'reply_count': i % 50,
                'like_count': i % 200,
                'quote_count': i % 30,
                'sentiment': sentiment,
                'topic': topic
            })
        
        return mock_tweets

if __name__ == '__main__':
    # Example usage
    service = MockTwitterService()
    
    # Search for tweets
    results = service.search_tweets(query='technology', max_results=5)
    
    print(f"Found {results['count']} tweets:")
    for tweet in results['tweets'][:3]:
        print(f"- {tweet['text'][:50]}... (Likes: {tweet['like_count']})")
    
    # Get rate limit info
    rate_info = service.get_rate_limit_info()
    print(f"\nRate limit remaining: {rate_info['remaining']}")