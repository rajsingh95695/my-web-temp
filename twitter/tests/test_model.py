"""Model tests for Twitter Sentiment Analysis Platform"""

import unittest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestSentimentModels(unittest.TestCase):
    """Test sentiment analysis models"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_texts = [
            'Great product! Loving the new features.',
            'Terrible service, would not recommend.',
            'The product is okay, nothing special.',
            'Outstanding performance and excellent quality.',
            'Very disappointed with the poor customer service.'
        ]
        
        self.expected_sentiments = ['positive', 'negative', 'neutral', 'positive', 'negative']
    
    def test_vader_sentiment(self):
        """Test VADER sentiment analysis"""
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        
        analyzer = SentimentIntensityAnalyzer()
        
        # Test individual texts
        test_cases = [
            ('Great product!', 0.5),  # Should be positive
            ('Terrible service', -0.5),  # Should be negative
            ('The product is okay', 0.0),  # Should be neutral
        ]
        
        for text, expected_direction in test_cases:
            scores = analyzer.polarity_scores(text)
            compound = scores['compound']
            
            if expected_direction > 0:
                self.assertGreater(compound, 0, f'Expected positive for: {text}')
            elif expected_direction < 0:
                self.assertLess(compound, 0, f'Expected negative for: {text}')
            else:
                self.assertAlmostEqual(compound, 0, delta=0.3, msg=f'Expected neutral for: {text}')
    
    def test_custom_sentiment_analyzer(self):
        """Test custom sentiment analyzer"""
        # Mock analyzer class
        class MockSentimentAnalyzer:
            def analyze(self, text):
                text_lower = text.lower()
                if 'great' in text_lower or 'excellent' in text_lower:
                    return {'sentiment': 'positive', 'score': 0.8}
                elif 'terrible' in text_lower or 'poor' in text_lower:
                    return {'sentiment': 'negative', 'score': -0.7}
                else:
                    return {'sentiment': 'neutral', 'score': 0.1}
        
        analyzer = MockSentimentAnalyzer()
        
        for text, expected in zip(self.sample_texts, self.expected_sentiments):
            result = analyzer.analyze(text)
            self.assertEqual(result['sentiment'], expected, 
                           f'Expected {expected} for: {text[:30]}...')
    
    def test_sentiment_thresholds(self):
        """Test sentiment classification thresholds"""
        from utils.sentiment_utils import classify_sentiment
        
        test_cases = [
            (0.8, 'positive'),
            (0.06, 'positive'),
            (0.05, 'neutral'),  # Boundary case
            (0.0, 'neutral'),
            (-0.04, 'neutral'),
            (-0.05, 'negative'),  # Boundary case
            (-0.5, 'negative'),
            (-0.9, 'negative')
        ]
        
        for score, expected in test_cases:
            result = classify_sentiment(score)
            self.assertEqual(result, expected, 
                           f'Score {score} should be {expected}, got {result}')
    
    def test_batch_sentiment_analysis(self):
        """Test batch sentiment analysis"""
        from utils.batch_analyzer import BatchSentimentAnalyzer
        
        analyzer = BatchSentimentAnalyzer()
        
        # Mock batch analysis
        with patch.object(analyzer, '_analyze_single') as mock_analyze:
            mock_analyze.side_effect = [
                {'sentiment': 'positive', 'score': 0.8},
                {'sentiment': 'negative', 'score': -0.7},
                {'sentiment': 'neutral', 'score': 0.1}
            ]
            
            results = analyzer.analyze_batch(['text1', 'text2', 'text3'])
            
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0]['sentiment'], 'positive')
            self.assertEqual(results[1]['sentiment'], 'negative')
            self.assertEqual(results[2]['sentiment'], 'neutral')
            
            self.assertEqual(mock_analyze.call_count, 3)
    
    def test_sentiment_statistics(self):
        """Test sentiment statistics calculation"""
        from utils.sentiment_stats import calculate_sentiment_statistics
        
        sentiment_results = [
            {'sentiment': 'positive', 'score': 0.8},
            {'sentiment': 'negative', 'score': -0.7},
            {'sentiment': 'positive', 'score': 0.6},
            {'sentiment': 'neutral', 'score': 0.1},
            {'sentiment': 'negative', 'score': -0.5}
        ]
        
        stats = calculate_sentiment_statistics(sentiment_results)
        
        self.assertEqual(stats['total'], 5)
        self.assertEqual(stats['positive_count'], 2)
        self.assertEqual(stats['negative_count'], 2)
        self.assertEqual(stats['neutral_count'], 1)
        self.assertAlmostEqual(stats['average_score'], (0.8 - 0.7 + 0.6 + 0.1 - 0.5) / 5, places=2)
        self.assertEqual(stats['dominant_sentiment'], 'positive')  # Tie-breaker

class TestModelPerformance(unittest.TestCase):
    """Test model performance metrics"""
    
    def test_accuracy_calculation(self):
        """Test accuracy calculation"""
        from utils.metrics import calculate_accuracy
        
        y_true = ['positive', 'negative', 'neutral', 'positive', 'negative']
        y_pred = ['positive', 'negative', 'neutral', 'negative', 'negative']  # One wrong
        
        accuracy = calculate_accuracy(y_true, y_pred)
        expected_accuracy = 4 / 5  # 80% accuracy
        
        self.assertAlmostEqual(accuracy, expected_accuracy, places=2)
    
    def test_confusion_matrix(self):
        """Test confusion matrix generation"""
        from utils.metrics import generate_confusion_matrix
        
        y_true = ['positive', 'negative', 'neutral', 'positive', 'negative']
        y_pred = ['positive', 'negative', 'neutral', 'negative', 'negative']
        
        cm = generate_confusion_matrix(y_true, y_pred)
        
        # Check matrix dimensions
        self.assertEqual(cm.shape, (3, 3))  # 3 sentiment classes
        
        # Check specific values
        # True positives for each class
        self.assertEqual(cm.loc['positive', 'positive'], 1)  # One correct positive
        self.assertEqual(cm.loc['negative', 'negative'], 2)  # Two correct negatives
        self.assertEqual(cm.loc['neutral', 'neutral'], 1)    # One correct neutral
        
        # Check misclassifications
        self.assertEqual(cm.loc['positive', 'negative'], 1)  # One positive misclassified as negative
    
    def test_precision_recall_f1(self):
        """Test precision, recall, and F1 score calculations"""
        from utils.metrics import calculate_precision_recall_f1
        
        y_true = ['positive', 'negative', 'neutral', 'positive', 'negative']
        y_pred = ['positive', 'negative', 'neutral', 'negative', 'negative']
        
        metrics = calculate_precision_recall_f1(y_true, y_pred)
        
        # Check that metrics are calculated for each class
        self.assertIn('positive', metrics)
        self.assertIn('negative', metrics)
        self.assertIn('neutral', metrics)
        
        # Check positive class metrics
        pos_metrics = metrics['positive']
        self.assertAlmostEqual(pos_metrics['precision'], 1.0)  # TP / (TP + FP) = 1 / (1 + 0)
        self.assertAlmostEqual(pos_metrics['recall'], 0.5)     # TP / (TP + FN) = 1 / (1 + 1)
        self.assertAlmostEqual(pos_metrics['f1'], 2/3)         # 2 * (1 * 0.5) / (1 + 0.5)
    
    def test_model_evaluation(self):
        """Test comprehensive model evaluation"""
        from utils.model_evaluator import ModelEvaluator
        
        evaluator = ModelEvaluator()
        
        # Mock predictions and true labels
        y_true = ['positive', 'negative', 'neutral'] * 10
        y_pred = ['positive', 'negative', 'neutral'] * 10  # Perfect predictions
        
        evaluation = evaluator.evaluate(y_true, y_pred)
        
        self.assertAlmostEqual(evaluation['accuracy'], 1.0)
        self.assertAlmostEqual(evaluation['macro_f1'], 1.0)
        self.assertAlmostEqual(evaluation['weighted_f1'], 1.0)
        
        # Check per-class metrics
        for sentiment in ['positive', 'negative', 'neutral']:
            class_metrics = evaluation['per_class'][sentiment]
            self.assertAlmostEqual(class_metrics['precision'], 1.0)
            self.assertAlmostEqual(class_metrics['recall'], 1.0)
            self.assertAlmostEqual(class_metrics['f1'], 1.0)

class TestModelPersistence(unittest.TestCase):
    """Test model saving and loading"""
    
    def test_model_serialization(self):
        """Test model serialization to disk"""
        import pickle
        import tempfile
        
        # Create a mock model
        mock_model = {
            'model_type': 'random_forest',
            'parameters': {'n_estimators': 100, 'max_depth': 20},
            'accuracy': 0.85,
            'features': ['feature1', 'feature2', 'feature3']
        }
        
        # Save model to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp_file:
            pickle.dump(mock_model, tmp_file)
            tmp_path = tmp_file.name
        
        try:
            # Load model from file
            with open(tmp_path, 'rb') as f:
                loaded_model = pickle.load(f)
            
            # Verify loaded model matches original
            self.assertEqual(loaded_model['model_type'], mock_model['model_type'])
            self.assertEqual(loaded_model['parameters'], mock_model['parameters'])
            self.assertEqual(loaded_model['accuracy'], mock_model['accuracy'])
            self.assertEqual(loaded_model['features'], mock_model['features'])
            
        finally:
            # Clean up temporary file
            import os
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_model_versioning(self):
        """Test model version management"""
        from utils.model_registry import ModelRegistry
        
        registry = ModelRegistry()
        
        # Mock model versions
        versions = [
            {'version': '1.0.0', 'accuracy': 0.82, 'timestamp': '2026-01-01'},
            {'version': '1.1.0', 'accuracy': 0.85, 'timestamp': '2026-02-01'},
            {'version': '2.0.0', 'accuracy': 0.88, 'timestamp': '2026-03-01'}
        ]
        
        # Test getting latest version
        latest = registry.get_latest_version(versions)
        self.assertEqual(latest['version'], '2.0.0')
        self.assertEqual(latest['accuracy'], 0.88)
        
        # Test version comparison
        self.assertTrue(registry.is_newer('2.0.0', '1.1.0'))
        self.assertFalse(registry.is_newer('1.0.0', '1.1.0'))
    
    def test_model_metadata(self):
        """Test model metadata management"""
        from utils.model_metadata import ModelMetadata
        
        metadata = ModelMetadata(
            name='sentiment_classifier_v2',
            version='2.1.0',
            model_type='random_forest',
            training_data_size=10000,
            accuracy=0.872,
            created_at='2026-04-24',
            author='Data Science Team'
        )
        
        # Test metadata serialization
        serialized = metadata.to_dict()
        
        self.assertEqual(serialized['name'], 'sentiment_classifier_v2')
        self.assertEqual(serialized['version'], '2.1.0')
        self.assertEqual(serialized['model_type'], 'random_forest')
        self.assertEqual(serialized['training_data_size'], 10000)
        self.assertEqual(serialized['accuracy'], 0.872)
        
        # Test metadata validation
        self.assertTrue(metadata.is_valid())
        
        # Test invalid metadata
        invalid_metadata = ModelMetadata(
            name='',
            version='invalid',
            model_type='',
            training_data_size=-100,
            accuracy=1.5,  # Invalid accuracy > 1.0
            created_at='',
            author=''
        )
        
        self.assertFalse(invalid_metadata.is_valid())

if __name__ == '__main__':
    unittest.main()