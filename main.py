import sys
import os
import logging
import time
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from config.app_config import Config
from modules import error_handling, database, menu, status_bar, toolbar, about  # Correct imports

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging to output to both a file and console
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', handlers=[
    logging.FileHandler(os.path.normpath("logs/app.log")),
    logging.StreamHandler()
])


def format_elapsed_time(elapsed_time):
    """
    Formats the elapsed time to display hours, minutes, and seconds.

    :param elapsed_time: Elapsed time in seconds.
    :return: A formatted string showing hours, minutes, and seconds.
    """
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(hours)}h {int(minutes)}m {seconds:.2f}s"


class MainWindow(QMainWindow):
    """
    MainWindow class responsible for setting up the main UI window 
    and initializing the application based on configuration settings.
    """
    def __init__(self, config, app):
        """Initialize the MainWindow and UI components."""
        super().__init__()
        self.config = config  # Pass the config from the main function
        self.app = app        # Store the app reference for future use
        self.init_ui()

    def init_ui(self):
        """
        Initializes the main user interface elements of the window 
        such as title, icon, window size, and optional features.
        """
        start_time = time.time()
        logging.info("Initializing UI")
        
        # Set window title and icon from the configuration (directly from app_config.py)
        self.setWindowTitle(self.config.get_about_info('name'))  # Fetch from app_config.py
        self.setWindowIcon(QIcon(self.config.get_about_info('icon')))  # Fetch from app_config.py
        
        # Set window size or maximize based on configuration (controlled by config.ini)
        self.setGeometry(100, 100, int(self.config.get_app_setting('screen_width')), int(self.config.get_app_setting('screen_height')))
        if self.config.get_app_setting('start_maximized') == 'True':
            self.showMaximized()
        
        # Initialize the menu, status bar, and toolbar based on configuration (controlled by app_config.py)
        if self.config.is_module_enabled('menu'):
            logging.info("Creating menu")
            menu.create_menu(self, self.config)
        if self.config.is_module_enabled('status_bar'):
            logging.info("Creating status bar")
            status_bar.create_status_bar(self)
        if self.config.is_module_enabled('toolbar'):
            logging.info("Creating toolbar")
            toolbar.create_toolbar(self)
        
        self.statusBar().showMessage("Status bar is visible")
        end_time = time.time()
        logging.info(f"UI initialized in {format_elapsed_time(end_time - start_time)}")


def main():
    """
    Main function that starts the application, initializes the 
    MainWindow, and optionally sets up logging and database connections.
    """
    start_time = None  # Declare start_time here to avoid UnboundLocalError

    try:
        config = Config()  # Initialize config, ensure Config does not take unnecessary arguments
        
        # Setup logging if enabled in the config
        if config.is_module_enabled('logging'):
            error_handling.setup_logging()

        logging.info("Starting application")
        start_time = time.time()
        
        # Initialize QApplication and MainWindow
        app = QApplication(sys.argv)
        window = MainWindow(config, app)  # Pass the config and app to MainWindow
        window.show()
        
        # Initialize the database if enabled in the config
        if config.is_module_enabled('database'):
            logging.info("Initializing database")
            database.main()  # Call the main function of the database module
        
        # Execute the application and handle errors
        app.exec()

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)  # Log errors with full traceback using exc_info

    finally:
        # Calculate and log the elapsed time
        if start_time is not None:
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f"Application ran for {format_elapsed_time(elapsed_time)}")
        logging.info("Closing application")


if __name__ == '__main__':
    main()