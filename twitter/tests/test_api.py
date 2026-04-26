"""API tests for Twitter Sentiment Analysis Platform"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTwitterAPI(unittest.TestCase):
    """Test Twitter API integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_response = {
            'status': 'success',
            'data': {
                'tweets': [
                    {'id': '1', 'text': 'Great product!', 'user': 'user1'},
                    {'id': '2', 'text': 'Terrible service', 'user': 'user2'}
                ],
                'next_cursor': 'next123'
            }
        }
    
    def test_api_connection(self):
        """Test API connection setup"""
        # Mock API connection
        mock_api = Mock()
        mock_api.connect.return_value = True
        mock_api.is_connected.return_value = True
        
        self.assertTrue(mock_api.connect())
        self.assertTrue(mock_api.is_connected())
    
    @patch('requests.get')
    def test_fetch_tweets_success(self, mock_get):
        """Test successful tweet fetching"""
        from utils.api_client import APIClient
        
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response
        mock_get.return_value = mock_response
        
        # Create API client and fetch tweets
        client = APIClient(api_key='test_key')
        result = client.fetch_tweets(query='test', limit=10)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['data']['tweets']), 2)
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_fetch_tweets_rate_limit(self, mock_get):
        """Test rate limit handling"""
        from utils.api_client import APIClient
        
        # Mock rate limit response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '60'}
        mock_get.return_value = mock_response
        
        client = APIClient(api_key='test_key')
        
        with self.assertRaises(Exception) as context:
            client.fetch_tweets(query='test', limit=10)
        
        self.assertIn('Rate limit', str(context.exception))
    
    def test_tweet_parsing(self):
        """Test tweet data parsing"""
        from utils.data_parser import parse_tweet
        
        raw_tweet = {
            'id': '123',
            'text': 'Great product! #awesome',
            'user': {'screen_name': 'user1'},
            'created_at': '2026-04-24T10:30:00Z',
            'retweet_count': 10,
            'favorite_count': 25
        }
        
        parsed = parse_tweet(raw_tweet)
        
        self.assertEqual(parsed['id'], '123')
        self.assertEqual(parsed['text'], 'Great product! #awesome')
        self.assertEqual(parsed['user'], 'user1')
        self.assertEqual(parsed['retweets'], 10)
        self.assertEqual(parsed['likes'], 25)
        self.assertIn('created_at', parsed)
    
    def test_batch_processing(self):
        """Test batch processing of tweets"""
        from utils.batch_processor import BatchProcessor
        
        processor = BatchProcessor(batch_size=2)
        tweets = [
            {'id': '1', 'text': 'Tweet 1'},
            {'id': '2', 'text': 'Tweet 2'},
            {'id': '3', 'text': 'Tweet 3'},
            {'id': '4', 'text': 'Tweet 4'}
        ]
        
        batches = list(processor.create_batches(tweets))
        
        self.assertEqual(len(batches), 2)
        self.assertEqual(len(batches[0]), 2)
        self.assertEqual(len(batches[1]), 2)
        self.assertEqual(batches[0][0]['id'], '1')
        self.assertEqual(batches[1][0]['id'], '3')

class TestSentimentAPI(unittest.TestCase):
    """Test sentiment analysis API"""
    
    def test_sentiment_endpoint(self):
        """Test sentiment analysis endpoint"""
        from utils.sentiment_analyzer import analyze_sentiment
        
        test_cases = [
            ('Great product!', 'positive'),
            ('Terrible service', 'negative'),
            ('The product is okay', 'neutral'),
            ('', 'neutral')  # Empty text
        ]
        
        for text, expected in test_cases:
            result = analyze_sentiment(text)
            self.assertEqual(result['sentiment'], expected)
    
    def test_sentiment_scores(self):
        """Test sentiment score calculations"""
        from utils.sentiment_analyzer import calculate_sentiment_score
        
        # Test positive sentiment
        pos_score = calculate_sentiment_score('Excellent amazing wonderful')
        self.assertGreater(pos_score, 0.5)
        
        # Test negative sentiment
        neg_score = calculate_sentiment_score('Terrible awful horrible')
        self.assertLess(neg_score, -0.5)
        
        # Test neutral sentiment
        neutral_score = calculate_sentiment_score('The weather is fine')
        self.assertGreaterEqual(neutral_score, -0.1)
        self.assertLessEqual(neutral_score, 0.1)
    
    def test_batch_sentiment(self):
        """Test batch sentiment analysis"""
        from utils.sentiment_analyzer import analyze_batch_sentiment
        
        texts = [
            'Great product!',
            'Terrible service',
            'Average experience',
            'Outstanding performance'
        ]
        
        results = analyze_batch_sentiment(texts)
        
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]['sentiment'], 'positive')
        self.assertEqual(results[1]['sentiment'], 'negative')
        
        # Check all results have required fields
        for result in results:
            self.assertIn('text', result)
            self.assertIn('sentiment', result)
            self.assertIn('score', result)
            self.assertIn('confidence', result)

class TestErrorHandling(unittest.TestCase):
    """Test API error handling"""
    
    def test_network_error(self):
        """Test network error handling"""
        from utils.api_client import APIClient
        from utils.exceptions import NetworkError
        
        client = APIClient(api_key='test_key')
        
        with patch('requests.get', side_effect=ConnectionError('Network error')):
            with self.assertRaises(NetworkError):
                client.fetch_tweets(query='test', limit=10)
    
    def test_invalid_response(self):
        """Test invalid response handling"""
        from utils.api_client import APIClient
        from utils.exceptions import InvalidResponseError
        
        client = APIClient(api_key='test_key')
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'error': 'Invalid request'}
            mock_get.return_value = mock_response
            
            with self.assertRaises(InvalidResponseError):
                client.fetch_tweets(query='test', limit=10)
    
    def test_authentication_error(self):
        """Test authentication error handling"""
        from utils.api_client import APIClient
        from utils.exceptions import AuthenticationError
        
        client = APIClient(api_key='invalid_key')
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.json.return_value = {'error': 'Invalid API key'}
            mock_get.return_value = mock_response
            
            with self.assertRaises(AuthenticationError):
                client.fetch_tweets(query='test', limit=10)

if __name__ == '__main__':
    unittest.main()