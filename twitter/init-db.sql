-- Twitter Sentiment Analysis Platform Database Schema
-- This script initializes the PostgreSQL database

-- Create tables for storing sentiment analysis results
CREATE TABLE IF NOT EXISTS sentiment_analysis (
    id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(100) UNIQUE NOT NULL,
    tweet_text TEXT NOT NULL,
    username VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment_score NUMERIC(5, 3),
    sentiment_label VARCHAR(20),
    confidence NUMERIC(5, 3),
    keywords TEXT[],
    source_query VARCHAR(255),
    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for analysis sessions
CREATE TABLE IF NOT EXISTS analysis_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_text VARCHAR(255) NOT NULL,
    tweet_count INTEGER NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'completed',
    user_ip VARCHAR(45),
    user_agent TEXT
);

-- Create table for aggregated statistics
CREATE TABLE IF NOT EXISTS daily_statistics (
    date DATE PRIMARY KEY,
    total_analyses INTEGER DEFAULT 0,
    positive_count INTEGER DEFAULT 0,
    negative_count INTEGER DEFAULT 0,
    neutral_count INTEGER DEFAULT 0,
    avg_sentiment_score NUMERIC(5, 3),
    most_common_keywords TEXT[]
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sentiment_analysis_tweet_id ON sentiment_analysis(tweet_id);
CREATE INDEX IF NOT EXISTS idx_sentiment_analysis_created_at ON sentiment_analysis(created_at);
CREATE INDEX IF NOT EXISTS idx_sentiment_analysis_sentiment_label ON sentiment_analysis(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_analysis_sessions_start_time ON analysis_sessions(start_time);

-- Create view for recent analyses
CREATE OR REPLACE VIEW recent_analyses AS
SELECT 
    sa.*,
    ases.query_text,
    ases.tweet_count
FROM sentiment_analysis sa
LEFT JOIN analysis_sessions ases ON sa.source_query = ases.query_text
WHERE sa.created_at > CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER BY sa.created_at DESC;

-- Create view for sentiment distribution
CREATE OR REPLACE VIEW sentiment_distribution AS
SELECT 
    sentiment_label,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM sentiment_analysis
WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '1 day'
GROUP BY sentiment_label
ORDER BY count DESC;

-- Insert sample data for demonstration (optional)
INSERT INTO sentiment_analysis (tweet_id, tweet_text, username, sentiment_score, sentiment_label, confidence, keywords, source_query)
VALUES 
    ('sample_1', 'I love this new product! It''s amazing!', 'user1', 0.85, 'positive', 0.92, ARRAY['love', 'amazing'], 'product review'),
    ('sample_2', 'This service is terrible and needs improvement', 'user2', -0.65, 'negative', 0.88, ARRAY['terrible', 'improvement'], 'service feedback'),
    ('sample_3', 'Just finished my morning coffee', 'user3', 0.12, 'neutral', 0.75, ARRAY['coffee'], 'daily routine')
ON CONFLICT (tweet_id) DO NOTHING;

-- Create user for application access (optional)
CREATE USER IF NOT EXISTS app_user WITH PASSWORD 'app_password';
GRANT SELECT, INSERT, UPDATE ON sentiment_analysis TO app_user;
GRANT SELECT, INSERT ON analysis_sessions TO app_user;
GRANT SELECT ON daily_statistics TO app_user;
GRANT SELECT ON recent_analyses TO app_user;
GRANT SELECT ON sentiment_distribution TO app_user;

-- Create function to update daily statistics
CREATE OR REPLACE FUNCTION update_daily_statistics()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO daily_statistics (date, total_analyses, positive_count, negative_count, neutral_count, avg_sentiment_score, most_common_keywords)
    VALUES (
        CURRENT_DATE,
        (SELECT COUNT(*) FROM sentiment_analysis WHERE DATE(created_at) = CURRENT_DATE),
        (SELECT COUNT(*) FROM sentiment_analysis WHERE DATE(created_at) = CURRENT_DATE AND sentiment_label = 'positive'),
        (SELECT COUNT(*) FROM sentiment_analysis WHERE DATE(created_at) = CURRENT_DATE AND sentiment_label = 'negative'),
        (SELECT COUNT(*) FROM sentiment_analysis WHERE DATE(created_at) = CURRENT_DATE AND sentiment_label = 'neutral'),
        (SELECT AVG(sentiment_score) FROM sentiment_analysis WHERE DATE(created_at) = CURRENT_DATE),
        (SELECT ARRAY_AGG(keyword) FROM (
            SELECT unnest(keywords) as keyword, COUNT(*) as count
            FROM sentiment_analysis 
            WHERE DATE(created_at) = CURRENT_DATE
            GROUP BY keyword
            ORDER BY count DESC
            LIMIT 5
        ) as top_keywords)
    )
    ON CONFLICT (date) DO UPDATE SET
        total_analyses = EXCLUDED.total_analyses,
        positive_count = EXCLUDED.positive_count,
        negative_count = EXCLUDED.negative_count,
        neutral_count = EXCLUDED.neutral_count,
        avg_sentiment_score = EXCLUDED.avg_sentiment_score,
        most_common_keywords = EXCLUDED.most_common_keywords;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to update statistics after each insert (optional)
-- DROP TRIGGER IF EXISTS update_stats_trigger ON sentiment_analysis;
-- CREATE TRIGGER update_stats_trigger
-- AFTER INSERT ON sentiment_analysis
-- FOR EACH ROW
-- EXECUTE FUNCTION update_daily_statistics();

COMMENT ON TABLE sentiment_analysis IS 'Stores individual tweet sentiment analysis results';
COMMENT ON TABLE analysis_sessions IS 'Tracks analysis sessions and queries';
COMMENT ON TABLE daily_statistics IS 'Aggregated daily statistics for reporting';