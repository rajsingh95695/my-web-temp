# API Usage Documentation

## Overview
The Twitter Sentiment Analysis Platform provides a comprehensive REST API for programmatic access to sentiment analysis capabilities. This document covers authentication, endpoints, request/response formats, and usage examples.

## Authentication

### API Key Authentication
All API requests require an API key in the header:
```
X-API-Key: your_api_key_here
```

### Rate Limits
- **Free Tier**: 100 requests per hour
- **Professional Tier**: 1,000 requests per hour
- **Enterprise Tier**: 10,000 requests per hour

## Endpoints

### 1. Analyze Single Tweet
**POST** `/api/v1/analyze/single`

**Request Body:**
```json
{
  "text": "Great product! Loving the new features.",
  "language": "en",
  "include_entities": true
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.87,
  "score": 0.72,
  "entities": ["product", "features"],
  "analysis_id": "anal_123456789"
}
```

### 2. Analyze Multiple Tweets
**POST** `/api/v1/analyze/batch`

**Request Body:**
```json
{
  "tweets": [
    {"id": "1", "text": "Great product!"},
    {"id": "2", "text": "Terrible service"}
  ],
  "batch_size": 100
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "1",
      "sentiment": "positive",
      "confidence": 0.87,
      "score": 0.72
    },
    {
      "id": "2",
      "sentiment": "negative",
      "confidence": 0.91,
      "score": -0.65
    }
  ],
  "summary": {
    "positive_count": 1,
    "negative_count": 1,
    "neutral_count": 0,
    "avg_sentiment": 0.035
  }
}
```

### 3. Get Historical Analysis
**GET** `/api/v1/historical/{date}`

**Parameters:**
- `date`: Date in YYYY-MM-DD format
- `limit`: Maximum results (default: 100)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "date": "2026-04-24",
  "total_analyses": 1250,
  "analyses": [...],
  "next_page": "/api/v1/historical/2026-04-24?offset=100&limit=100"
}
```

### 4. Real-time Streaming
**WebSocket** `/ws/v1/sentiment`

**Connection:**
```javascript
const ws = new WebSocket('wss://api.example.com/ws/v1/sentiment');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.sentiment);
};
```

**Stream Format:**
```json
{
  "tweet_id": "123456789",
  "text": "Live tweet analysis",
  "sentiment": "positive",
  "confidence": 0.82,
  "timestamp": "2026-04-24T10:30:00Z"
}
```

## Error Handling

### Common Error Codes
- **400**: Bad Request - Invalid parameters
- **401**: Unauthorized - Missing or invalid API key
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - System error

### Error Response Format
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit of 100 requests per hour exceeded",
    "details": {
      "limit": 100,
      "remaining": 0,
      "reset_at": "2026-04-24T11:30:00Z"
    }
  }
}
```

## SDKs and Libraries

### Python SDK
```python
from sentiment_sdk import Client

client = Client(api_key="your_key")
result = client.analyze("Great product!")
print(result.sentiment)  # "positive"
```

### JavaScript SDK
```javascript
import { SentimentClient } from 'sentiment-sdk';

const client = new SentimentClient('your_key');
const result = await client.analyze('Great product!');
console.log(result.sentiment); // "positive"
```

## Best Practices

1. **Implement Retry Logic**: Handle rate limits with exponential backoff
2. **Cache Results**: Cache analysis results for identical text
3. **Batch Requests**: Use batch endpoints for multiple analyses
4. **Monitor Usage**: Track API usage to avoid rate limits
5. **Error Handling**: Implement comprehensive error handling

## Support
For API support, contact:
- Email: api-support@example.com
- Documentation: https://docs.example.com
- Status Page: https://status.example.com