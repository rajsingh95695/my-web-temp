# Deployment Guide

## Overview
This document provides comprehensive instructions for deploying the Twitter Sentiment Analysis Platform in various environments, from local development to production cloud deployment.

## Prerequisites

### System Requirements
- **CPU**: 4+ cores (8+ recommended for production)
- **RAM**: 8GB minimum (16GB+ recommended)
- **Storage**: 50GB+ free disk space
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2

### Software Dependencies
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.9+
- **Node.js**: 18+ (for frontend)
- **PostgreSQL**: 14+
- **Redis**: 7+

## Deployment Methods

### 1. Local Development (Docker Compose)

#### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-org/twitter-sentiment-platform.git
cd twitter-sentiment-platform

# Copy environment configuration
cp .env.example .env

# Update environment variables
nano .env

# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

#### Service Ports
- **API Server**: http://localhost:8000
- **Frontend Dashboard**: http://localhost:3000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Adminer**: http://localhost:8080

### 2. Kubernetes Deployment

#### Helm Chart Installation
```bash
# Add the Helm repository
helm repo add sentiment-platform https://charts.example.com

# Install the chart
helm install sentiment-platform sentiment-platform/twitter-sentiment \
  --namespace sentiment \
  --create-namespace \
  --values values-production.yaml
```

#### Production Values (values-production.yaml)
```yaml
replicaCount: 3
image:
  repository: ghcr.io/your-org/twitter-sentiment-api
  tag: latest
  pullPolicy: Always

resources:
  limits:
    cpu: 1000m
    memory: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

database:
  enabled: true
  type: postgresql
  size: 100Gi

redis:
  enabled: true
  size: 10Gi

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: api.sentiment.example.com
      paths:
        - path: /
          pathType: Prefix
```

### 3. Cloud Deployment (AWS)

#### Terraform Configuration
```hcl
module "sentiment_platform" {
  source = "github.com/your-org/terraform-aws-sentiment"

  environment = "production"
  region      = "us-east-1"
  
  vpc_cidr = "10.0.0.0/16"
  
  rds_instance_class = "db.t3.large"
  rds_storage_gb     = 100
  
  ecs_cluster_name = "sentiment-cluster"
  ecs_service_count = 3
  
  alb_internal = false
  domain_name  = "sentiment.example.com"
}
```

#### AWS Services Used
- **ECS/Fargate**: Container orchestration
- **RDS PostgreSQL**: Managed database
- **ElastiCache Redis**: Caching layer
- **ALB**: Load balancing
- **S3**: File storage
- **CloudWatch**: Monitoring and logging

## Configuration

### Environment Variables

#### Required Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379

# API Keys
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
RAPIDAPI_KEY=your_rapidapi_key

# Application
SECRET_KEY=your_secret_key_here
ENVIRONMENT=production
LOG_LEVEL=INFO
```

#### Optional Variables
```bash
# Email/SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_password

# Monitoring
SENTRY_DSN=your_sentry_dsn
NEW_RELIC_LICENSE_KEY=your_new_relic_key

# External Services
OPENAI_API_KEY=your_openai_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

## Database Setup

### Initial Migration
```bash
# Run database migrations
docker-compose exec api python manage.py migrate

# Create superuser
docker-compose exec api python manage.py createsuperuser

# Load initial data
docker-compose exec api python manage.py loaddata initial_data.json
```

### Database Backups
```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups/sentiment"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > $BACKUP_DIR/backup_$DATE.sql
gzip $BACKUP_DIR/backup_$DATE.sql

# Keep last 30 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

## Monitoring and Maintenance

### Health Checks
```bash
# API Health Check
curl -f http://localhost:8000/health

# Database Health Check
docker-compose exec db pg_isready

# Redis Health Check
docker-compose exec redis redis-cli ping
```

### Logging
```bash
# View application logs
docker-compose logs -f api

# View database logs
docker-compose logs -f db

# Export logs for analysis
docker-compose logs --tail=1000 api > api_logs_$(date +%Y%m%d).log
```

### Performance Monitoring
- **Prometheus**: Metrics collection at http://localhost:9090
- **Grafana**: Dashboards at http://localhost:3001
- **Alert Manager**: Configured for critical alerts

## Security Considerations

### 1. Network Security
- Use VPC with private subnets for database
- Configure security groups with minimum required access
- Enable SSL/TLS for all external connections

### 2. Data Encryption
- Enable encryption at rest for databases
- Use TLS 1.3 for data in transit
- Encrypt sensitive environment variables

### 3. Access Control
- Implement least privilege principle
- Use IAM roles for AWS resources
- Regular rotation of API keys and credentials

### 4. Compliance
- GDPR compliance for user data
- Regular security audits
- Penetration testing quarterly

## Troubleshooting

### Common Issues

#### 1. Database Connection Failures
```bash
# Check database status
docker-compose exec db pg_isready

# Check connection from API
docker-compose exec api python -c "
import psycopg2
try:
    conn = psycopg2.connect('$DATABASE_URL')
    print('Connection successful')
except Exception as e:
    print(f'Connection failed: {e}')
"
```

#### 2. Memory Issues
```bash
# Check memory usage
docker stats

# Increase memory limits in docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 2G
```

#### 3. Rate Limiting
```bash
# Check API rate limits
curl -H "X-API-Key: $API_KEY" http://localhost:8000/api/rate-limit

# Implement exponential backoff in client code
```

## Support
For deployment assistance, contact:
- **DevOps Team**: devops@example.com
- **Documentation**: https://docs.example.com/deployment
- **Emergency Support**: +1-800-123-4567 (24/7)