import json
import os
import time
import logging
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import QDir


def apply_theme(app, theme_file):
    """
    Applies the selected theme to the application by setting the QPalette
    and applying a custom stylesheet to menus, toolbars, and message boxes.

    :param app: The QApplication instance.
    :param theme_file: Path to the theme JSON file.
    """
    try:
        # Normalize the theme file path for uniform logging
        theme_file = os.path.normpath(theme_file)
        logging.info(f"Applying theme from file: {theme_file}")

        # Check if the theme file is empty
        if os.path.getsize(theme_file) == 0:
            raise ValueError(f"Theme file {theme_file} is empty")

        # Load theme data from the JSON file
        with open(theme_file, 'r') as file:
            theme_data = json.load(file)

        # Validate that all required fields are present in the JSON data
        required_fields = [
            'window_background', 'window_text', 
            'button_background', 'button_text', 
            'menu_background', 'menu_text', 
            'highlight_color'
        ]
        missing_fields = [field for field in required_fields if field not in theme_data]
        if missing_fields:
            raise ValueError(f"Missing required fields in theme file {theme_file}: {', '.join(missing_fields)}")

        # Create a new QPalette object and apply colors from the theme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(theme_data['window_background']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(theme_data['window_text']))
        palette.setColor(QPalette.ColorRole.Button, QColor(theme_data['button_background']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme_data['button_text']))
        app.setPalette(palette)

        # Apply custom QSS (Qt Style Sheets) for additional UI elements
        qss = f"""
        QMenuBar {{
            background-color: {theme_data['menu_background']};
            color: {theme_data['menu_text']};
        }}
        QMenuBar::item {{
            background-color: {theme_data['menu_background']};
            color: {theme_data['menu_text']};
        }}
        QMenuBar::item:selected {{
            background-color: {theme_data['highlight_color']};
            color: {theme_data['menu_text']};
        }}
        QMenu {{
            background-color: {theme_data['menu_background']};
            color: {theme_data['menu_text']};
        }}
        QMenu::item:selected {{
            background-color: {theme_data['highlight_color']};
            color: {theme_data['menu_text']};
        }}
        QToolBar {{
            background-color: {theme_data['menu_background']};
        }}
        QMessageBox {{
            background-color: {theme_data['window_background']};
            color: {theme_data['window_text']};
        }}
        QPushButton {{
            background-color: {theme_data['button_background']};
            color: {theme_data['button_text']};
        }}
        """
        app.setStyleSheet(qss)

        logging.info("Theme applied successfully.")
        QMessageBox.information(None, "Theme Applied", "The theme has been applied successfully.")

    except json.JSONDecodeError as json_err:
        logging.error(f"Invalid JSON format in {theme_file}: {json_err}")
        QMessageBox.critical(None, "Error", f"Failed to apply theme: Invalid JSON format in {theme_file}")
    except ValueError as val_err:
        logging.error(f"Theme application error: {val_err}")
        QMessageBox.critical(None, "Error", f"Failed to apply theme: {val_err}")
    except Exception as e:
        logging.error(f"Failed to apply theme: {e}")
        QMessageBox.critical(None, "Error", f"Failed to apply theme: {e}")


def load_theme(app):
    """
    Opens a file dialog to select a theme file from the resources/styles directory
    and applies the selected theme.

    :param app: The QApplication instance.
    """
    theme_dir = os.path.join(os.path.dirname(__file__), '../resources/styles')

    # Ensure the theme directory exists
    if not os.path.exists(theme_dir):
        os.makedirs(theme_dir)
        logging.info(f"Created theme directory: {theme_dir}")
        QMessageBox.information(None, "Theme Directory", f"Created directory: {theme_dir}")

    # Open file dialog in the styles directory to select a theme file
    theme_file, _ = QFileDialog.getOpenFileName(None, "Open Theme File", theme_dir, "Theme Files (*.json)")

    if theme_file:
        theme_file = os.path.normpath(theme_file)  # Normalize the path for consistent formatting
        logging.info(f"Selected theme file: {theme_file}")
        apply_theme(app, theme_file)
    else:
        logging.info("No theme file selected.")


def main():
    """
    Main function to simulate the application running and handle the theme
    loading and application with proper runtime logging.
    """
    # Start time
    start_time = time.time()

    # Your application code goes here
    logging.info("Starting application")

    # Simulate application runtime (example: load and apply theme)
    app = None  # Replace this with your actual QApplication instance
    load_theme(app)

    # End time and calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Log the formatted elapsed time
    logging.info(f"Application ran for {format_elapsed_time(elapsed_time)}")

    logging.info("Closing application")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

    # Run the main function
    main()
