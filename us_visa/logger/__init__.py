from from_root import from_root
from datetime import datetime
import os
import logging

# Create log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Logs directory name
log_dir = "logs"

# Full logs directory path from project root
logs_dir_path = os.path.join(from_root(), log_dir)

# Create logs directory if it doesn't exist
os.makedirs(logs_dir_path, exist_ok=True)

# Full log file path
logs_path = os.path.join(logs_dir_path, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)