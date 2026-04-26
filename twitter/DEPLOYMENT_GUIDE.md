# Twitter Sentiment Analysis Platform - Complete Deployment Guide

## 📋 Overview

This guide provides complete deployment instructions for the Twitter Sentiment Analysis Platform. The platform is containerized using Docker and can be deployed locally, on-premises, or in the cloud.

## 🚀 Quick Start Deployment

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose
- Git (optional)
- 4GB RAM minimum, 8GB recommended

### Step-by-Step Deployment

#### Option 1: Using Automated Scripts (Recommended)

**Windows:**
```bash
deploy.bat
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

#### Option 2: Manual Deployment

1. **Clone or copy the project**
   ```bash
   git clone <repository-url>
   cd twitter-sentiment-analysis
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file and add your RapidAPI key
   ```

3. **Build and start services**
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

4. **Verify deployment**
   ```bash
   docker-compose ps
   ```

## 🔧 Configuration

### Environment Variables (.env file)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `RAPIDAPI_KEY` | RapidAPI Twitter API key | - | **Yes** |
| `DB_PASSWORD` | PostgreSQL password | `admin123` | No |
| `GRAFANA_PASSWORD` | Grafana admin password | `admin123` | No |

### Getting RapidAPI Key
1. Visit [RapidAPI Twitter API](https://rapidapi.com/omarmhaimdat/api/twitter-api45)
2. Sign up for a free account
3. Subscribe to the API
4. Copy your API key to `.env` file

## 📊 Services Overview

| Service | Port | Purpose | Access URL |
|---------|------|---------|------------|
| Streamlit App | 8501 | Main dashboard | http://localhost:8501 |
| PostgreSQL | 5432 | Database | localhost:5432 |
| Redis | 6379 | Caching | localhost:6379 |
| Grafana | 3000 | Monitoring dashboard | http://localhost:3000 |
| Prometheus | 9090 | Metrics collection | http://localhost:9090 |

## 🐳 Docker Architecture

### Multi-Stage Build
- **Builder stage**: Installs dependencies and builds Python packages
- **Production stage**: Minimal image with only runtime dependencies

### Container Structure
```
twitter-sentiment-app (Streamlit)
├── PostgreSQL (Database)
├── Redis (Cache)
├── Nginx (Reverse Proxy - optional)
├── Prometheus (Metrics)
└── Grafana (Visualization)
```

## 📈 Monitoring & Observability

### Built-in Monitoring Stack
1. **Prometheus**: Collects metrics from all services
2. **Grafana**: Visualizes metrics with pre-configured dashboards
3. **Health Checks**: Automatic health monitoring for all containers

### Accessing Monitoring
- Grafana: http://localhost:3000 (admin/admin123)
- Prometheus: http://localhost:9090

### Key Metrics Monitored
- API response times
- Tweet fetch success rates
- Database connection pool
- Memory and CPU usage
- Error rates and exceptions

## 🗄️ Database Management

### PostgreSQL Configuration
- Database: `sentiment_db`
- User: `admin`
- Password: Set in `.env` file
- Port: `5432`

### Database Schema
The database includes:
- `sentiment_analysis`: Individual tweet analysis results
- `analysis_sessions`: Analysis session tracking
- `daily_statistics`: Aggregated daily metrics

### Backup and Restore
```bash
# Backup database
docker exec twitter-sentiment-db pg_dump -U admin sentiment_db > backup.sql

# Restore database
docker exec -i twitter-sentiment-db psql -U admin sentiment_db < backup.sql
```

## 🔒 Security Considerations

### API Key Security
- API keys stored in `.streamlit/secrets.toml` (not in version control)
- Environment variables for sensitive data
- Never commit secrets to Git

### Network Security
- Services communicate via internal Docker network
- External access only through defined ports
- Optional SSL/TLS via Nginx

### User Authentication
- Streamlit app: No authentication by default (add if needed)
- Grafana: Password protected
- Database: Password protected

## 📱 Production Deployment

### Cloud Deployment Options

#### AWS (EC2 + ECS)
```bash
# Build and push to ECR
aws ecr create-repository --repository-name twitter-sentiment
docker build -t twitter-sentiment .
docker tag twitter-sentiment:latest <account-id>.dkr.ecr.<region>.amazonaws.com/twitter-sentiment:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/twitter-sentiment:latest

# Deploy with ECS
```

#### Azure (Container Instances)
```bash
az container create \
  --resource-group myResourceGroup \
  --name twitter-sentiment \
  --image twitter-sentiment:latest \
  --ports 8501 \
  --environment-variables RAPIDAPI_KEY=$RAPIDAPI_KEY
```

#### Google Cloud (Cloud Run)
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/twitter-sentiment
gcloud run deploy twitter-sentiment \
  --image gcr.io/PROJECT-ID/twitter-sentiment \
  --platform managed \
  --port 8501
```

### Scaling Considerations
- **Horizontal Scaling**: Deploy multiple Streamlit instances behind load balancer
- **Database Scaling**: Consider managed PostgreSQL service (RDS, Cloud SQL)
- **Cache Scaling**: Redis cluster for high availability

## 🛠️ Maintenance

### Common Operations

#### Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d
```

#### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f twitter-sentiment-app

# Follow logs with timestamps
docker-compose logs --tail=100 --timestamps
```

#### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

#### Restart Services
```bash
# Restart specific service
docker-compose restart twitter-sentiment-app

# Restart all services
docker-compose restart
```

### Health Checks
```bash
# Check service health
docker-compose ps

# Check container logs
docker-compose logs --tail=50

# Check API health
curl http://localhost:8501/_stcore/health
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "Port already in use"
```bash
# Find process using port
netstat -ano | findstr :8501

# Kill process or change port in docker-compose.yml
```

#### 2. "Docker daemon not running"
- Start Docker Desktop
- On Linux: `sudo systemctl start docker`

#### 3. "API key not working"
- Verify RapidAPI key in `.env` file
- Check API quota and subscription status
- Test API directly: `curl -H "X-RapidAPI-Key: YOUR_KEY" ...`

#### 4. "Database connection failed"
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View database logs
docker-compose logs postgres

# Reset database (warning: data loss)
docker-compose down -v
docker-compose up -d
```

#### 5. "Memory issues"
- Increase Docker memory allocation (Docker Desktop Settings)
- Reduce services in `docker-compose.yml`
- Monitor with `docker stats`

### Debugging Commands
```bash
# Enter container shell
docker exec -it twitter-sentiment-app /bin/bash

# Check container resources
docker stats

# Inspect container configuration
docker inspect twitter-sentiment-app

# View network configuration
docker network inspect twitter-network
```

## 📚 Additional Resources

### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Documentation](https://docs.docker.com/)
- [RapidAPI Twitter API Docs](https://rapidapi.com/omarmhaimdat/api/twitter-api45)

### Monitoring Dashboards
Pre-configured Grafana dashboards include:
1. **Application Performance**: Response times, error rates
2. **System Resources**: CPU, memory, disk usage
3. **API Metrics**: Request counts, success rates
4. **Database Performance**: Query times, connections

### Backup Strategy
1. **Daily database backups** (cron job)
2. **Configuration backups** (Git repository)
3. **Log rotation** (Docker log drivers)
4. **Volume backups** (cloud storage)

## 🎯 Performance Optimization

### Caching Strategy
- Redis cache for API responses (30-minute TTL)
- Browser caching for static assets
- Database query optimization with indexes

### Database Optimization
```sql
-- Regularly run maintenance
VACUUM ANALYZE sentiment_analysis;

-- Monitor slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### Resource Limits
Adjust in `docker-compose.yml`:
```yaml
services:
  twitter-sentiment-app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
```

## 🔄 CI/CD Pipeline (Optional)

### GitHub Actions Example
```yaml
name: Deploy Twitter Sentiment Analysis

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker-compose build
        
      - name: Deploy to server
        run: |
          scp -r . user@server:/opt/twitter-sentiment
          ssh user@server "cd /opt/twitter-sentiment && docker-compose up -d"
```

## 📞 Support

### Getting Help
1. Check the [GitHub Issues](https://github.com/your-repo/issues)
2. Review the troubleshooting section above
3. Contact the development team

### Reporting Issues
When reporting issues, include:
- Docker and Docker Compose versions
- Error messages and logs
- Steps to reproduce
- Environment details

---

## 🎉 Deployment Complete!

Your Twitter Sentiment Analysis Platform is now deployed and ready to use. Access the dashboard at http://localhost:8501 and start analyzing Twitter sentiment in real-time!

**Next Steps:**
1. Configure your RapidAPI key in the `.env` file
2. Access the Grafana dashboard to set up monitoring
3. Explore the API documentation for advanced usage
4. Consider setting up SSL/TLS for production use

**Remember:** For production deployments, always:
- Use strong passwords
- Enable SSL/TLS encryption
- Set up proper backups
- Monitor resource usage
- Keep Docker and dependencies updated