import logging
import json
import os
from typing import Optional, Dict, Any
from packages.LocalAgentCore.remedy_log import RemedyLog


class RemedyLogger:
    def __init__(self, log_dir: str = "remedy_logs", log_file_prefix: str = "remedy"):
        self.log_dir = log_dir
        self.log_file_prefix = log_file_prefix
        os.makedirs(self.log_dir, exist_ok=True)
        self.logger = self._setup_logger()

    def _get_log_file_path(self) -> str:
        """Generates a unique log file path based on the current timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S%f")
        log_file_name = f"{self.log_file_prefix}_{timestamp}.json"
        return os.path.join(self.log_dir, log_file_name)

    def _setup_logger(self) -> logging.Logger:
        """Sets up a logger that writes to both a file and the console."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # File handler
        log_file_path = self._get_log_file_path()
        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def log_remedy(self, remedy_log: RemedyLog):
        """Logs a remedy log entry to the log file."""
        try:
            log_entry = remedy_log.to_dict()
            # Convert datetime objects to ISO format strings
            log_entry['timestamp'] = log_entry['timestamp'].isoformat()
            json_record = json.dumps(log_entry)
            self.logger.info(json_record)
        except Exception as e:
            self.logger.error(f"Error logging remedy: {e}")

    def log(self, level:str, message:str):
        """Logs a simple message at the given log level"""
        getattr(self.logger, level.lower())(message)


# Example usage (can be removed later)
if __name__ == '__main__':
    import datetime
    remedy_logger = RemedyLogger()
    remedy_log = RemedyLog(
        timestamp=datetime.datetime.now(),
        user_id="user123",
        module="TestModule",
        instrument_ids=["instrument1", "instrument2"],
        workflow_id="workflow456",
        data={"key1": "value1", "key2": "value2"},
        log_level="INFO",
        message="This is a test log message"
    )
    remedy_logger.log_remedy(remedy_log)
    remedy_logger.log("WARNING", "This is a simple warning message")
