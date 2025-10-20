import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(name: str = 'app', log_dir: str = 'logs') -> logging.Logger:
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler for all logs (rotating)
    all_logs_file = os.path.join(log_dir, 'app.log')
    file_handler = RotatingFileHandler(
        all_logs_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # File handler for errors only
    error_logs_file = os.path.join(log_dir, 'errors.log')
    error_handler = RotatingFileHandler(
        error_logs_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)

    # File handler for warnings
    warning_logs_file = os.path.join(log_dir, 'warnings.log')
    warning_handler = RotatingFileHandler(
        warning_logs_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    warning_handler.setLevel(logging.WARNING)
    warning_handler.addFilter(lambda record: record.levelno == logging.WARNING)
    warning_handler.setFormatter(detailed_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(console_handler)

    return logger


# Create default logger instance
app_logger = setup_logger()
