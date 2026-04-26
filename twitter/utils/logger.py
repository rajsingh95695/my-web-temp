"""Logging utilities for Twitter Sentiment Analysis Platform"""

import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional, Dict, Any
import json
from datetime import datetime
import os

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields from record
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        return json.dumps(log_data)

class StructuredLogger:
    """Structured logger with multiple handlers"""
    
    def __init__(self, name: str, log_level: str = 'INFO', 
                 log_file: Optional[str] = None,
                 max_file_size: int = 10485760,  # 10MB
                 backup_count: int = 5):
        """
        Initialize structured logger
        
        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (optional)
            max_file_size: Maximum log file size in bytes
            backup_count: Number of backup files to keep
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler if log file specified
        if log_file:
            # Create directory if it doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_file_size,
                backupCount=backup_count
            )
            file_handler.setLevel(getattr(logging, log_level.upper()))
            json_formatter = JSONFormatter()
            file_handler.setFormatter(json_formatter)
            self.logger.addHandler(file_handler)
        
        # Create error file handler for ERROR and CRITICAL logs
        if log_file:
            error_log_file = log_file.replace('.log', '_error.log')
            error_handler = TimedRotatingFileHandler(
                error_log_file,
                when='midnight',
                interval=1,
                backupCount=30
            )
            error_handler.setLevel(logging.ERROR)
            error_formatter = JSONFormatter()
            error_handler.setFormatter(error_formatter)
            self.logger.addHandler(error_handler)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with extra fields"""
        self.logger.debug(message, extra={'extra': kwargs})
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message with extra fields"""
        self.logger.info(message, extra={'extra': kwargs})
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with extra fields"""
        self.logger.warning(message, extra={'extra': kwargs})
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message with extra fields"""
        self.logger.error(message, extra={'extra': kwargs})
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message with extra fields"""
        self.logger.critical(message, extra={'extra': kwargs})
    
    def exception(self, message: str, exc_info: Optional[Exception] = None, **kwargs) -> None:
        """Log exception with traceback"""
        if exc_info:
            self.logger.exception(message, exc_info=exc_info, extra={'extra': kwargs})
        else:
            self.logger.exception(message, extra={'extra': kwargs})

class PerformanceLogger:
    """Logger for performance metrics"""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.metrics = {}
    
    def start_timer(self, operation: str) -> None:
        """Start timer for an operation"""
        self.metrics[operation] = {
            'start_time': datetime.utcnow(),
            'end_time': None,
            'duration': None
        }
    
    def stop_timer(self, operation: str) -> float:
        """Stop timer and return duration in seconds"""
        if operation not in self.metrics:
            raise KeyError(f"No timer started for operation: {operation}")
        
        end_time = datetime.utcnow()
        start_time = self.metrics[operation]['start_time']
        duration = (end_time - start_time).total_seconds()
        
        self.metrics[operation].update({
            'end_time': end_time,
            'duration': duration
        })
        
        # Log the performance metric
        self.logger.info(
            f"Operation '{operation}' completed",
            operation=operation,
            duration=duration,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat()
        )
        
        return duration
    
    def log_metric(self, name: str, value: float, **kwargs) -> None:
        """Log a performance metric"""
        self.logger.info(
            f"Performance metric: {name}",
            metric_name=name,
            metric_value=value,
            **kwargs
        )
    
    def log_memory_usage(self) -> None:
        """Log current memory usage"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        self.logger.info(
            "Memory usage",
            rss_mb=memory_info.rss / 1024 / 1024,
            vms_mb=memory_info.vms / 1024 / 1024,
            percent=process.memory_percent()
        )

class AuditLogger:
    """Logger for audit trails"""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
    
    def log_api_call(self, endpoint: str, method: str, status_code: int,
                    user_id: Optional[str] = None, duration: Optional[float] = None,
                    **kwargs) -> None:
        """Log API call for audit trail"""
        self.logger.info(
            f"API {method} {endpoint} - Status: {status_code}",
            audit_type='api_call',
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            user_id=user_id,
            duration=duration,
            **kwargs
        )
    
    def log_data_access(self, data_type: str, operation: str, user_id: Optional[str] = None,
                       record_count: Optional[int] = None, **kwargs) -> None:
        """Log data access for audit trail"""
        self.logger.info(
            f"Data access: {operation} on {data_type}",
            audit_type='data_access',
            data_type=data_type,
            operation=operation,
            user_id=user_id,
            record_count=record_count,
            **kwargs
        )
    
    def log_security_event(self, event_type: str, severity: str, description: str,
                          user_id: Optional[str] = None, ip_address: Optional[str] = None,
                          **kwargs) -> None:
        """Log security event for audit trail"""
        self.logger.warning(
            f"Security event: {event_type} - {description}",
            audit_type='security_event',
            event_type=event_type,
            severity=severity,
            description=description,
            user_id=user_id,
            ip_address=ip_address,
            **kwargs
        )

# Global logger instance
_logger_instance: Optional[StructuredLogger] = None

def get_logger(name: str = 'twitter_sentiment', **kwargs) -> StructuredLogger:
    """Get or create global logger instance"""
    global _logger_instance
    
    if _logger_instance is None:
        # Default configuration
        config = {
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'log_file': os.getenv('LOG_FILE', 'logs/app.log'),
            'max_file_size': int(os.getenv('LOG_MAX_SIZE', 10485760)),
            'backup_count': int(os.getenv('LOG_BACKUP_COUNT', 5))
        }
        config.update(kwargs)
        
        _logger_instance = StructuredLogger(name, **config)
    
    return _logger_instance

def get_performance_logger() -> PerformanceLogger:
    """Get performance logger instance"""
    logger = get_logger('performance')
    return PerformanceLogger(logger)

def get_audit_logger() -> AuditLogger:
    """Get audit logger instance"""
    logger = get_logger('audit')
    return AuditLogger(logger)

# Convenience functions
def debug(message: str, **kwargs) -> None:
    """Convenience function for debug logging"""
    get_logger().debug(message, **kwargs)

def info(message: str, **kwargs) -> None:
    """Convenience function for info logging"""
    get_logger().info(message, **kwargs)

def warning(message: str, **kwargs) -> None:
    """Convenience function for warning logging"""
    get_logger().warning(message, **kwargs)

def error(message: str, **kwargs) -> None:
    """Convenience function for error logging"""
    get_logger().error(message, **kwargs)

def critical(message: str, **kwargs) -> None:
    """Convenience function for critical logging"""
    get_logger().critical(message, **kwargs)

def exception(message: str, exc_info: Optional[Exception] = None, **kwargs) -> None:
    """Convenience function for exception logging"""
    get_logger().exception(message, exc_info=exc_info, **kwargs)

if __name__ == '__main__':
    # Example usage
    logger = get_logger('example')
    
    logger.info("Application started", version="2.1.0", environment="development")
    
    # Performance logging example
    perf_logger = get_performance_logger()
    perf_logger.start_timer('data_processing')
    
    # Simulate some work
    import time
    time.sleep(0.1)
    
    duration = perf_logger.stop_timer('data_processing')
    print(f"Data processing took {duration:.3f} seconds")
    
    # Audit logging example
    audit_logger = get_audit_logger()
    audit_logger.log_api_call(
        endpoint='/api/analyze',
        method='POST',
        status_code=200,
        user_id='user123',
        duration=0.15
    )
    
    # Error logging example
    try:
        raise ValueError("Example error")
    except ValueError as e:
        logger.error("An error occurred", error_type=type(e).__name__, error_message=str(e))
    
    logger.info("Application shutdown")