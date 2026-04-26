"""Text preprocessing utilities for sentiment analysis"""

import re
import string
from typing import List, Optional
import emoji

class TextPreprocessor:
    """Preprocess text for sentiment analysis"""
    
    def __init__(self, remove_stopwords: bool = True, language: str = 'en'):
        self.remove_stopwords = remove_stopwords
        self.language = language
        self.stopwords = self._load_stopwords()
    
    def _load_stopwords(self) -> set:
        """Load stopwords for the specified language"""
        # Basic English stopwords
        english_stopwords = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'shall', 'should', 'can', 'could', 'may',
            'might', 'must', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        return english_stopwords
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ''
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove user mentions
        text = re.sub(r'@\w+', '', text)
        
        # Remove hashtag symbols (keep text)
        text = re.sub(r'#', '', text)
        
        # Convert emojis to text
        text = emoji.demojize(text, delimiters=(' ', ' '))
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        text = self.clean_text(text)
        tokens = text.split()
        
        if self.remove_stopwords:
            tokens = [token for token in tokens if token not in self.stopwords]
        
        return tokens
    
    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation from text"""
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text"""
        return ' '.join(text.split())

def preprocess_pipeline(texts: List[str], **kwargs) -> List[str]:
    """Batch preprocessing pipeline"""
    preprocessor = TextPreprocessor(**kwargs)
    return [preprocessor.clean_text(text) for text in texts]

if __name__ == '__main__':
    # Example usage
    preprocessor = TextPreprocessor()
    sample_text = "Great product! Loving the new features. #awesome @user123 https://example.com"
    cleaned = preprocessor.clean_text(sample_text)
    print(f'Original: {sample_text}')
    print(f'Cleaned: {cleaned}')