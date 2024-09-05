import configparser
import os
import logging
from modules.error_handling import setup_logging
from config.settings_dialog import SettingsDialog  
import config.settings as app_settings  # Import settings from the config folder

class Config:
    def __init__(self, config_file='config/config.ini'):
        """
        Initialize the Config class.
        
        :param config_file: Path to the configuration file.
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        # Load About and Module info from settings.py
        self.about_info = app_settings.about_info
        self.modules = app_settings.modules

        # Ensure the config directory exists
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            logging.info(f"Created config directory: {config_dir}")

        # Load the config.ini file or create a default one if not found
        if not os.path.exists(self.config_file):
            self.create_default_config()

        self.load_config()

        # Setup logging if the logging module is enabled
        if self.is_module_enabled('logging'):
            self.setup_logging()

    def load_config(self):
        """
        Loads the application configuration from the config.ini file.
        """
        try:
            self.config.read(self.config_file)
            logging.info(f"Configuration loaded from {os.path.normpath(self.config_file)}")
        except Exception as e:
            logging.error(f"Failed to load config file: {e}")

    def create_default_config(self):
        """
        Creates a default configuration file with APP and LOGGING sections.
        """
        try:
            self.config['APP'] = app_settings.app_defaults
            self.config['LOGGING'] = app_settings.logging_defaults
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
            logging.info(f"Default config created at: {self.config_file}")
        except Exception as e:
            logging.error(f"Failed to create default config: {e}")

    def setup_logging(self):
        """
        Setup logging configuration based on settings loaded from config.ini.
        """
        try:
            log_file = self.get_logging_setting('log_file', app_settings.logging_defaults['log_file'])
            max_bytes = int(self.get_logging_setting('max_bytes', app_settings.logging_defaults['max_bytes']))
            backup_count = int(self.get_logging_setting('backup_count', app_settings.logging_defaults['backup_count']))
            logging_level = self.get_logging_setting('level', app_settings.logging_defaults['level']).upper()

            setup_logging(log_file=log_file, max_bytes=max_bytes, backup_count=backup_count)
            logging.info(f"Logging setup with level: {logging_level}, log file: {log_file}")
        except Exception as e:
            logging.error(f"Failed to setup logging: {e}")

    def get_about_info(self, key):
        """
        Retrieves information from the about section (e.g., app name, version, author).
        
        :param key: The key to retrieve from about_info.
        :return: The corresponding value or 'Unknown' if not found.
        """
        return self.about_info.get(key, "Unknown")

    def get_app_setting(self, option, fallback=None):
        """
        Retrieves a setting from the APP section in config.ini.
        
        :param option: The option name (e.g., start_maximized, screen_width).
        :param fallback: Fallback value if the option is not found.
        :return: The value of the option or the fallback.
        """
        return self.get('APP', option, fallback=fallback)

    def get_logging_setting(self, option, fallback=None):
        """
        Retrieves a setting from the LOGGING section in config.ini.
        
        :param option: The option name (e.g., log_file, max_bytes, level).
        :param fallback: Fallback value if the option is not found.
        :return: The value of the option or the fallback.
        """
        return self.get('LOGGING', option, fallback=fallback)

    def is_module_enabled(self, module):
        """
        Checks if a specific module is enabled based on settings.
        
        :param module: The module to check (e.g., logging, database).
        :return: True if the module is enabled, False otherwise.
        """
        return self.modules.get(module, False)

    def get(self, section, option, fallback=None):
        """
        Generic method to retrieve a configuration value from a section with a fallback.
        
        :param section: The section in the config file.
        :param option: The option to retrieve from the section.
        :param fallback: Fallback value if the section or option is not found.
        :return: The configuration value or the fallback.
        """
        try:
            return self.config.get(section, option, fallback=fallback)
        except configparser.NoSectionError:
            logging.error(f"Section '{section}' not found in config file.")
        except configparser.NoOptionError:
            logging.error(f"Option '{option}' not found in section '{section}' of config file.")
        return fallback
