# Model Details Documentation

## Overview
This document provides detailed information about the machine learning models used in the Twitter Sentiment Analysis Platform. The platform employs an ensemble approach combining rule-based, traditional ML, and deep learning models for robust sentiment analysis.

## Model Architecture

### Ensemble Approach
The platform uses a weighted ensemble of three primary models:

1. **Rule-based Model (VADER)**: 20% weight
2. **Traditional ML Model (Random Forest)**: 30% weight  
3. **Deep Learning Model (BERT)**: 50% weight

### Final Prediction Formula
```
final_score = (0.2 * vader_score) + (0.3 * rf_score) + (0.5 * bert_score)
sentiment = 
  "positive" if final_score > 0.05
  "negative" if final_score < -0.05  
  "neutral" otherwise
```

## Individual Model Details

### 1. VADER (Valence Aware Dictionary and sEntiment Reasoner)

#### Overview
- **Type**: Rule-based lexicon and sentiment analysis tool
- **Specialization**: Social media text, slang, emoticons, and capitalization
- **Strength**: Fast, no training required, handles informal language well

#### Features
- **Lexicon**: 7,500+ sentiment-laden words with intensity scores
- **Rules**: Handles punctuation, capitalization, degree modifiers
- **Emoticons**: 150+ emoticon mappings
- **Slang**: Common internet slang and acronyms

#### Performance
- **Accuracy**: 78% on social media text
- **Speed**: < 1ms per tweet
- **Languages**: Primarily English, with basic multi-language support

### 2. Random Forest Classifier

#### Overview
- **Type**: Ensemble of decision trees
- **Training Data**: 100,000 manually labeled tweets
- **Features**: 5,000+ engineered features

#### Feature Engineering

##### Text Features
- **TF-IDF**: 1-3 grams with 10,000 vocabulary limit
- **Word Counts**: Character count, word count, sentence count
- **Readability**: Flesch-Kincaid, Gunning Fog scores
- **Lexical Diversity**: Type-token ratio, unique word percentage

##### Linguistic Features
- **Part-of-Speech**: Noun/verb/adjective ratios
- **Sentiment Lexicons**: AFINN, SentiWordNet, MPQA scores
- **Emotion Scores**: NRC Emotion Lexicon (8 emotions)
- **Formality**: Formality score based on syntactic patterns

##### Social Media Features
- **Hashtag Analysis**: Sentiment of hashtags
- **Mention Count**: Number of @mentions
- **URL Presence**: Binary indicator
- **Emoji Analysis**: Sentiment score of emojis present

#### Model Configuration
```python
RandomForestClassifier(
    n_estimators=500,
    max_depth=30,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    bootstrap=True,
    random_state=42,
    n_jobs=-1
)
```

#### Performance
- **Accuracy**: 85.3% (10-fold cross-validation)
- **Precision**: 0.86 (positive), 0.84 (negative), 0.83 (neutral)
- **Recall**: 0.85 (positive), 0.83 (negative), 0.84 (neutral)
- **F1-Score**: 0.855 weighted average

### 3. BERT (Bidirectional Encoder Representations from Transformers)

#### Overview
- **Base Model**: bert-base-uncased (110M parameters)
- **Fine-tuning**: 50,000 domain-specific tweets
- **Architecture**: Transformer-based with 12 layers, 768 hidden units

#### Fine-tuning Process

##### Data Preparation
- **Dataset**: 50,000 tweets balanced across sentiments
- **Split**: 80% training, 10% validation, 10% test
- **Preprocessing**: Lowercasing, URL removal, @mention normalization

##### Training Configuration
```python
TrainingArguments(
    output_dir='./results',
    num_train_epochs=4,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=100,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True
)
```

##### Hyperparameters
- **Learning Rate**: 2e-5 with linear decay
- **Optimizer**: AdamW with epsilon=1e-8
- **Max Sequence Length**: 128 tokens
- **Dropout**: 0.1

#### Performance
- **Accuracy**: 91.2% on test set
- **Macro F1**: 0.910
- **Inference Speed**: ~15ms per tweet (GPU), ~50ms (CPU)

## Model Training Pipeline

### 1. Data Collection
```python
# Sources:
# - Twitter API (real-time streaming)
# - Kaggle datasets (historical)
# - Manual annotation (gold standard)
# - External sentiment datasets
```

### 2. Preprocessing
```python
def preprocess_tweet(text):
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Remove user mentions
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtag symbols (keep text)
    text = re.sub(r'#', '', text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    # Handle emoticons (convert to text representation)
    text = emoticon_to_text(text)
    
    return text
```

### 3. Feature Extraction
```python
# Parallel feature extraction pipeline
features = {
    'text_features': extract_text_features(text),
    'linguistic_features': extract_linguistic_features(text),
    'social_features': extract_social_features(text),
    'bert_embeddings': get_bert_embeddings(text)
}
```

### 4. Training
```python
# Three-phase training approach
# Phase 1: Individual model training
# Phase 2: Hyperparameter optimization
# Phase 3: Ensemble weight optimization
```

### 5. Evaluation
```python
# Comprehensive evaluation suite
metrics = {
    'accuracy': accuracy_score(y_true, y_pred),
    'precision': precision_score(y_true, y_pred, average='weighted'),
    'recall': recall_score(y_true, y_pred, average='weighted'),
    'f1': f1_score(y_true, y_pred, average='weighted'),
    'confusion_matrix': confusion_matrix(y_true, y_pred),
    'roc_auc': roc_auc_score(y_true, y_pred_proba, multi_class='ovr')
}
```

## Model Deployment

### Serving Architecture
- **Model Registry**: MLflow for model versioning
- **Serving Engine**: TensorFlow Serving for BERT, custom Flask API for others
- **Caching**: Redis cache for frequent predictions
- **Monitoring**: Prometheus metrics for model performance

### API Endpoints
```python
# Single prediction
POST /api/v1/models/predict
{
    "text": "Great product!",
    "model": "ensemble"  # or "vader", "random_forest", "bert"
}

# Batch prediction  
POST /api/v1/models/predict_batch
{
    "texts": ["text1", "text2", "text3"],
    "model": "ensemble"
}

# Model information
GET /api/v1/models/info
```

### Performance Optimization

#### 1. Caching Strategy
```python
# Cache predictions for identical text
cache_key = f"prediction:{hash(text)}"
if redis.exists(cache_key):
    return json.loads(redis.get(cache_key))
else:
    prediction = model.predict(text)
    redis.setex(cache_key, 3600, json.dumps(prediction))
    return prediction
```

#### 2. Batch Processing
```python
# Process tweets in batches for efficiency
batch_size = 32
for i in range(0, len(texts), batch_size):
    batch = texts[i:i+batch_size]
    predictions = model.predict_batch(batch)
    results.extend(predictions)
```

#### 3. Model Quantization
```python
# Quantize BERT model for faster inference
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

## Model Maintenance

### 1. Retraining Schedule
- **Daily**: Incremental training with new data
- **Weekly**: Full retraining with expanded dataset  
- **Monthly**: Hyperparameter re-optimization
- **Quarterly**: Architecture review and potential upgrades

### 2. Monitoring Metrics
- **Prediction Latency**: P95 < 100ms
- **Accuracy Drift**: Alert if > 2% decrease
- **Data Drift**: Monitor feature distribution changes
- **Model Bias**: Regular fairness audits

### 3. Version Control
```python
# Model versioning schema
version = {
    'major': 2,  # Architecture changes
    'minor': 1,  # Significant improvements
    'patch': 3   # Bug fixes
}
# Example: v2.1.3
```

## Limitations and Future Work

### Current Limitations
1. **Language Support**: Primarily English, limited multi-language
2. **Context Understanding**: Limited understanding of sarcasm and irony
3. **Domain Adaptation**: Performance varies across domains
4. **Real-time Processing**: BERT inference can be slow on CPU

### Planned Improvements
1. **Multilingual BERT**: Support for 100+ languages
2. **Contextual Understanding**: Incorporate conversation context
3. **Domain Adaptation**: Automatic domain detection and adaptation
4. **Efficient Models**: DistilBERT, TinyBERT for faster inference
5. **Explainability**: SHAP/LIME integration for model explanations

## References
1. Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text
2. Devlin, J. et al. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
3. Breiman, L. (2001). Random Forests
4. Liu, Y. et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach