from PyQt6.QtWidgets import (QDialog, QLabel, QLineEdit, QCheckBox, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QFormLayout, QTabWidget, 
                             QComboBox, QWidget, QSpacerItem, QSizePolicy, QFileDialog)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import config.settings as app_settings
import logging
from PIL import Image  # Ensure Pillow is installed: pip install pillow

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Settings")

        # Initialize the fields dictionary
        self.fields = {}

        # Main layout with tabs
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Add tabs for different sections
        self.add_about_tab("About Info", app_settings.about_info)
        self.add_module_tab("Modules", app_settings.modules)
        self.add_app_defaults_tab("App Defaults", app_settings.app_defaults)
        self.add_logging_tab("Logging Settings", app_settings.logging_defaults)

        # Add tabs to the main layout
        self.layout.addWidget(self.tabs)

        # Save and Cancel buttons
        self.create_buttons()

        self.setLayout(self.layout)

        # Set initial window size and restrict resizing
        self.setMinimumSize(500, 500)
        self.adjustSize()

    def add_about_tab(self, tab_title, settings_dict):
        """ Add a tab for 'About Info' section, including an icon that can be changed. """
        tab = QWidget()
        layout = QFormLayout()

        for key, value in settings_dict.items():
            if key == 'icon':
                self.icon_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
                pixmap = QPixmap(value).scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio)
                self.icon_label.setPixmap(pixmap)
                self.icon_label.setFixedSize(256, 256)

                # Enable double-click to change the icon
                self.icon_label.mouseDoubleClickEvent = self.change_icon

                layout.addRow(QLabel("App Icon"), self.icon_label)
            else:
                field = QLineEdit(str(value))
                self.fields[(tab_title, key)] = field
                layout.addRow(QLabel(key.capitalize()), field)

        tab.setLayout(layout)
        self.tabs.addTab(tab, tab_title)

    def change_icon(self, event):
        """ Handle double-click event to change the app icon. """
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_path, _ = file_dialog.getOpenFileName(self, "Select App Icon")

        if file_path:
            try:
                # Check image dimensions using Pillow
                with Image.open(file_path) as img:
                    if img.size != (256, 256):
                        raise ValueError("Image dimensions must be 256x256 pixels.")
                
                # If valid, update the icon
                pixmap = QPixmap(file_path).scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio)
                self.icon_label.setPixmap(pixmap)
                app_settings.about_info['icon'] = file_path  # Update the icon path in settings
                logging.info(f"Icon updated to {file_path}")
            except Exception as e:
                logging.error(f"Invalid icon: {e}")
                self.show_error(f"Invalid image: {str(e)}")

    def show_error(self, message):
        """ Show an error message dialog. """
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Error")
        error_label = QLabel(message)
        error_layout = QVBoxLayout()
        error_layout.addWidget(error_label)
        close_button = QPushButton("Close")
        close_button.clicked.connect(error_dialog.close)
        error_layout.addWidget(close_button)
        error_dialog.setLayout(error_layout)
        error_dialog.exec()

    def add_module_tab(self, tab_title, modules_dict):
        """ Add a tab for the 'Modules' section with checkboxes. """
        tab = QWidget()
        layout = QVBoxLayout()

        # Adding module checkboxes
        for key, value in modules_dict.items():
            checkbox = QCheckBox(key.capitalize())
            checkbox.setChecked(value)
            self.fields[(tab_title, key)] = checkbox
            layout.addWidget(checkbox)

        # Spacer at the bottom for cleaner layout
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        tab.setLayout(layout)
        self.tabs.addTab(tab, tab_title)

    def add_app_defaults_tab(self, tab_title, settings_dict):
        """ Add a tab for 'App Defaults' section with fields, including Dark Mode toggle. """
        tab = QWidget()
        layout = QFormLayout()

        # Adding window settings fields
        for key, value in settings_dict.items():
            if key == "start_maximized":
                field = QComboBox()
                field.addItems(["True", "False"])
                field.setCurrentText("True" if value else "False")
            elif key == "dark_mode":
                field = QCheckBox("Enable Dark Mode")
                field.setChecked(value == "True")
            elif isinstance(value, bool):
                field = QCheckBox()
                field.setChecked(value)
            else:
                field = QLineEdit(str(value))

            self.fields[(tab_title, key)] = field
            layout.addRow(QLabel(key.capitalize()), field)

        tab.setLayout(layout)
        self.tabs.addTab(tab, tab_title)

    def add_logging_tab(self, tab_title, logging_dict):
        """ Add a tab for 'Logging Settings' with a mix of fields and dropdowns. """
        tab = QWidget()
        layout = QFormLayout()

        for key, value in logging_dict.items():
            if key == "level":
                field = QComboBox()
                field.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
                field.setCurrentText(str(value))
            elif isinstance(value, bool):
                field = QCheckBox()
                field.setChecked(value)
            else:
                field = QLineEdit(str(value))

            self.fields[(tab_title, key)] = field
            layout.addRow(QLabel(key.capitalize()), field)

        tab.setLayout(layout)
        self.tabs.addTab(tab, tab_title)

    def create_buttons(self):
        """ Add Save and Cancel buttons at the bottom of the dialog. """
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.close)

        buttons_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(buttons_layout)

    def save_settings(self):
        """ Save the modified settings back to the settings.py file. """
        try:
            for key in app_settings.about_info:
                if key != 'icon':
                    app_settings.about_info[key] = self.fields[("About Info", key)].text().strip()

            for key in app_settings.modules:
                app_settings.modules[key] = self.fields[("Modules", key)].isChecked()

            for key in app_settings.app_defaults:
                field = self.fields[("App Defaults", key)]
                if key == "dark_mode":
                    app_settings.app_defaults[key] = "True" if field.isChecked() else "False"
                elif isinstance(field, QComboBox):
                    app_settings.app_defaults[key] = field.currentText()
                else:
                    app_settings.app_defaults[key] = field.text().strip()

            for key in app_settings.logging_defaults:
                field = self.fields[("Logging Settings", key)]
                if isinstance(field, QComboBox):
                    if key == "level":
                        app_settings.logging_defaults[key] = field.currentText()
                    else:
                        app_settings.logging_defaults[key] = field.currentText() == "True"
                else:
                    app_settings.logging_defaults[key] = field.text().strip()

            self.save_to_file()
            logging.info("Settings successfully saved.")
            self.close()

        except Exception as e:
            logging.error(f"Failed to save settings: {e}", exc_info=True)

    def save_to_file(self):
        """ Write the updated settings back to the settings.py file. """
        with open('config/settings.py', 'w') as f:
            f.write(f"about_info = {app_settings.about_info}\n")
            f.write(f"modules = {app_settings.modules}\n")
            f.write(f"app_defaults = {app_settings.app_defaults}\n")
            f.write(f"logging_defaults = {app_settings.logging_defaults}\n")
        logging.info("Settings file updated.")
