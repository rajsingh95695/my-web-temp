"""FastAPI application for Twitter Sentiment Analysis API"""

from fastapi import FastAPI, HTTPException, Depends, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uvicorn
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Twitter Sentiment Analysis API",
    description="REST API for analyzing sentiment of Twitter data",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TweetAnalysisRequest(BaseModel):
    """Request model for tweet analysis"""
    text: str = Field(..., min_length=1, max_length=280, description="Tweet text to analyze")
    include_confidence: bool = Field(True, description="Include confidence scores")
    language: str = Field("en", description="Language of the text")

class BatchAnalysisRequest(BaseModel):
    """Request model for batch analysis"""
    tweets: List[TweetAnalysisRequest] = Field(..., max_items=100, description="List of tweets to analyze")
    batch_id: Optional[str] = Field(None, description="Optional batch identifier")

class TwitterSearchRequest(BaseModel):
    """Request model for Twitter search"""
    query: str = Field(..., min_length=1, description="Search query")
    max_results: int = Field(100, ge=1, le=1000, description="Maximum number of results")
    analyze_sentiment: bool = Field(True, description="Perform sentiment analysis on results")

class AnalysisResponse(BaseModel):
    """Response model for analysis"""
    text: str
    sentiment: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    score: float = Field(..., ge=-1.0, le=1.0)
    analysis_id: str
    timestamp: datetime

class BatchAnalysisResponse(BaseModel):
    """Response model for batch analysis"""
    batch_id: str
    total_tweets: int
    processed_tweets: int
    results: List[AnalysisResponse]
    summary: Dict[str, Any]
    processing_time: float

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    uptime: float
    services: Dict[str, str]

# Mock services (in production, import actual services)
class SentimentAnalyzer:
    """Mock sentiment analyzer"""
    
    @staticmethod
    def analyze(text: str, language: str = "en") -> Dict[str, Any]:
        """Analyze sentiment of text"""
        # Mock analysis - in production, use actual ML models
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['great', 'excellent', 'awesome', 'love']):
            sentiment = "positive"
            score = 0.8
            confidence = 0.9
        elif any(word in text_lower for word in ['bad', 'terrible', 'awful', 'hate']):
            sentiment = "negative"
            score = -0.7
            confidence = 0.85
        else:
            sentiment = "neutral"
            score = 0.1
            confidence = 0.7
        
        return {
            "sentiment": sentiment,
            "score": score,
            "confidence": confidence,
            "analysis_id": f"anal_{datetime.utcnow().timestamp()}"
        }

class TwitterService:
    """Mock Twitter service"""
    
    @staticmethod
    def search_tweets(query: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Search for tweets"""
        # Mock data - in production, call Twitter API
        mock_tweets = []
        for i in range(min(max_results, 10)):
            mock_tweets.append({
                "id": f"tweet_{i}",
                "text": f"Sample tweet about {query} #{i}",
                "user": f"user_{i}",
                "created_at": datetime.utcnow().isoformat(),
                "retweets": i * 2,
                "likes": i * 5
            })
        return mock_tweets

# API endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Twitter Sentiment Analysis API",
        "version": "2.1.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="2.1.0",
        timestamp=datetime.utcnow(),
        uptime=3600.0,  # Mock uptime
        services={
            "sentiment_analyzer": "operational",
            "twitter_api": "operational",
            "database": "operational",
            "cache": "operational"
        }
    )

@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_tweet(request: TweetAnalysisRequest):
    """Analyze sentiment of a single tweet"""
    try:
        logger.info(f"Analyzing tweet: {request.text[:50]}...")
        
        # Perform sentiment analysis
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze(request.text, request.language)
        
        response = AnalysisResponse(
            text=request.text,
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            score=result["score"],
            analysis_id=result["analysis_id"],
            timestamp=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/batch", response_model=BatchAnalysisResponse, tags=["Analysis"])
async def analyze_batch(request: BatchAnalysisRequest, background_tasks: BackgroundTasks):
    """Analyze sentiment of multiple tweets in batch"""
    try:
        logger.info(f"Processing batch with {len(request.tweets)} tweets")
        
        batch_id = request.batch_id or f"batch_{datetime.utcnow().timestamp()}"
        results = []
        
        # Process each tweet
        for tweet_request in request.tweets:
            analyzer = SentimentAnalyzer()
            result = analyzer.analyze(tweet_request.text, tweet_request.language)
            
            analysis_response = AnalysisResponse(
                text=tweet_request.text,
                sentiment=result["sentiment"],
                confidence=result["confidence"],
                score=result["score"],
                analysis_id=result["analysis_id"],
                timestamp=datetime.utcnow()
            )
            results.append(analysis_response)
        
        # Calculate summary statistics
        sentiment_counts = {}
        confidence_sum = 0
        score_sum = 0
        
        for result in results:
            sentiment_counts[result.sentiment] = sentiment_counts.get(result.sentiment, 0) + 1
            confidence_sum += result.confidence
            score_sum += result.score
        
        summary = {
            "sentiment_distribution": sentiment_counts,
            "average_confidence": confidence_sum / len(results) if results else 0,
            "average_score": score_sum / len(results) if results else 0,
            "dominant_sentiment": max(sentiment_counts, key=sentiment_counts.get) if sentiment_counts else "neutral"
        }
        
        response = BatchAnalysisResponse(
            batch_id=batch_id,
            total_tweets=len(request.tweets),
            processed_tweets=len(results),
            results=results,
            summary=summary,
            processing_time=0.5  # Mock processing time
        )
        
        # Background task for logging/analytics
        background_tasks.add_task(log_batch_analysis, batch_id, len(request.tweets))
        
        return response
        
    except Exception as e:
        logger.error(f"Batch analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@app.post("/search", tags=["Twitter"])
async def search_tweets(request: TwitterSearchRequest):
    """Search for tweets and optionally analyze sentiment"""
    try:
        logger.info(f"Searching tweets for query: {request.query}")
        
        # Search for tweets
        twitter_service = TwitterService()
        tweets = twitter_service.search_tweets(request.query, request.max_results)
        
        response = {
            "query": request.query,
            "total_results": len(tweets),
            "tweets": tweets
        }
        
        # Analyze sentiment if requested
        if request.analyze_sentiment and tweets:
            analyzer = SentimentAnalyzer()
            analyzed_tweets = []
            
            for tweet in tweets:
                analysis = analyzer.analyze(tweet["text"])
                tweet["sentiment"] = analysis["sentiment"]
                tweet["sentiment_score"] = analysis["score"]
                tweet["sentiment_confidence"] = analysis["confidence"]
                analyzed_tweets.append(tweet)
            
            response["tweets"] = analyzed_tweets
            
            # Add sentiment summary
            sentiments = [tweet["sentiment"] for tweet in analyzed_tweets]
            sentiment_counts = {sentiment: sentiments.count(sentiment) for sentiment in set(sentiments)}
            response["sentiment_summary"] = sentiment_counts
        
        return response
        
    except Exception as e:
        logger.error(f"Tweet search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Tweet search failed: {str(e)}")

@app.get("/analyses/{analysis_id}", tags=["Analysis"])
async def get_analysis(analysis_id: str):
    """Get analysis results by ID"""
    # Mock implementation
    return {
        "analysis_id": analysis_id,
        "status": "completed",
        "result": {
            "sentiment": "positive",
            "score": 0.8,
            "confidence": 0.9
        },
        "retrieved_at": datetime.utcnow().isoformat()
    }

@app.get("/metrics", tags=["Metrics"])
async def get_metrics(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get API usage metrics"""
    # Mock metrics
    return {
        "total_analyses": 1250,
        "average_processing_time": 0.15,
        "success_rate": 0.98,
        "sentiment_distribution": {
            "positive": 650,
            "negative": 300,
            "neutral": 300
        },
        "period": {
            "start": start_date or "2026-04-01",
            "end": end_date or "2026-04-24"
        }
    }

# Background tasks
async def log_batch_analysis(batch_id: str, tweet_count: int):
    """Background task to log batch analysis"""
    logger.info(f"Batch {batch_id} completed with {tweet_count} tweets")
    # In production, log to database or analytics service

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Handle application startup"""
    logger.info("Starting Twitter Sentiment Analysis API...")
    # Initialize services, connect to databases, etc.

@app.on_event("shutdown")
async def shutdown_event():
    """Handle application shutdown"""
    logger.info("Shutting down Twitter Sentiment Analysis API...")
    # Cleanup resources, close connections, etc.

if __name__ == "__main__":
    uvicorn.run(
        "api.fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )