import logging
import os

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(filename='logs/app.log', level=logging.INFO,  # Changed to INFO level
                        format='%(asctime)s:%(levelname)s:%(message)s')

def log_error(error):
    logging.error(error)
