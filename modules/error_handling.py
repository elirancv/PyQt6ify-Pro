import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_file='logs/app.log', max_bytes=5 * 1024 * 1024, backup_count=3):
    """
    Set up logging for the application with log rotation.
    
    :param log_file: The path to the log file.
    :param max_bytes: Maximum size of the log file before rotation (in bytes).
    :param backup_count: Number of backup log files to keep.
    """
    # Ensure the logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set up the log format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(filename)s:%(lineno)d]"

    # Create a rotating file handler
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Create a stream handler to output to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(log_format))

    # Set up the root logger
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])

    logging.info("Logging has been set up.")


def log_error(error, exc_info=True):
    """
    Log an error with optional exception info.
    
    :param error: The error message to log.
    :param exc_info: Whether to include the full exception traceback (default: True).
    """
    logging.error(error, exc_info=exc_info)


def log_warning(warning):
    """
    Log a warning message.
    
    :param warning: The warning message to log.
    """
    logging.warning(warning)


def log_info(info):
    """
    Log an informational message.
    
    :param info: The informational message to log.
    """
    logging.info(info)


def log_debug(debug_message):
    """
    Log a debug message.
    
    :param debug_message: The debug message to log.
    """
    logging.debug(debug_message)


# Example usage
if __name__ == "__main__":
    setup_logging()

    try:
        # Simulate application behavior for testing logging
        log_info("Application started.")
        
        # Simulate a warning
        log_warning("This is a warning message.")

        # Simulate an error
        raise ValueError("This is a simulated error.")

    except Exception as e:
        log_error("An error occurred", exc_info=True)

    log_info("Application finished.")
