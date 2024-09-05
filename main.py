import sys
import os
import logging
import time
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from config.app_config import Config
from config.settings_dialog import SettingsDialog
from modules import error_handling, database, menu, status_bar, toolbar, about

# Ensure the logs directory exists before configuring logging
os.makedirs('logs', exist_ok=True)

# Configure logging to output to both a file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler(os.path.normpath("logs/app.log")),
        logging.StreamHandler()
    ]
)

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

        # Fetch window settings
        screen_width = int(self.config.get_app_setting('screen_width', 800))
        screen_height = int(self.config.get_app_setting('screen_height', 600))
        start_maximized = self.config.get_app_setting('start_maximized', 'True') == 'True'

        # Set window size or maximize based on configuration
        if start_maximized:
            logging.info("Maximizing window as per configuration.")
            self.showMaximized()  # Maximize the window if the setting is True
        else:
            logging.info("Setting window size to %sx%s.", screen_width, screen_height)
            self.setGeometry(100, 100, screen_width, screen_height)
            self.show()  # Show window in defined size if maximization is False

        # Initialize the menu, status bar, and toolbar based on configuration (controlled by app_config.py)
        self.initialize_components()

        self.statusBar().showMessage("Status bar is visible")
        end_time = time.time()
        logging.info(f"UI initialized in {format_elapsed_time(end_time - start_time)}")

    def initialize_components(self):
        """
        Initializes components like menu, status bar, and toolbar
        based on the configuration settings.
        """
        try:
            if self.config.is_module_enabled('menu'):
                logging.info("Creating menu")
                menu.create_menu(self, self.config)

            if self.config.is_module_enabled('status_bar'):
                logging.info("Creating status bar")
                status_bar.create_status_bar(self)

            if self.config.is_module_enabled('toolbar'):
                logging.info("Creating toolbar")
                toolbar.create_toolbar(self)
        except AttributeError as e:
            logging.error(f"Error initializing components: {e}")
            raise


def main():
    """
    Main function that starts the application, initializes the 
    MainWindow, and optionally sets up logging and database connections.
    """
    start_time = time.time()

    try:
        # Load configuration
        config = Config()

        # Setup logging based on configuration
        if config.is_module_enabled('logging'):
            error_handling.setup_logging()

        logging.info("Starting application")

        # Initialize QApplication and MainWindow
        app = QApplication(sys.argv)
        window = MainWindow(config, app)

        # Initialize the database if enabled
        if config.is_module_enabled('database'):
            logging.info("Initializing database")
            database.main()

        # Execute the application
        app.exec()

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

    finally:
        # Log the total application runtime
        elapsed_time = time.time() - start_time
        logging.info(f"Application ran for {format_elapsed_time(elapsed_time)}")
        logging.info("Closing application")

if __name__ == '__main__':
    main()
