"""
Logger for the HR Assistant.
"""
import logging
import os
from datetime import datetime

LOGS_DIR = 'hr_logs'

# 1. Generate the sub-folder path (e.g., 'hr_logs/20260908')
DAILY_LOGS_DIR = os.path.join(LOGS_DIR, datetime.now().strftime("%Y%m%d"))

# 2. This will properly create 'hr_logs' and the nested '20260908' folder at the same time
os.makedirs(DAILY_LOGS_DIR, exist_ok=True)

# 3. Create the log file path inside the correct directory
_run_started = datetime.now().strftime("%Y%m%d_%H%M%S")
Run_LOG_FILE = os.path.join(DAILY_LOGS_DIR, f'hr_assistant_{_run_started}.log') 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler(Run_LOG_FILE),
        logging.StreamHandler()
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logging.getLogger(name)  