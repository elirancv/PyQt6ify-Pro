import configparser
import os
import logging
from modules.error_handling import setup_logging
from config.settings_dialog import SettingsDialog  


# Import settings from the config folder
import config.settings as app_settings

class Config:
    def __init__(self, config_file='config/config.ini'):
        """
        Initialize the Config class.
        
        :param config_file: Path to the configuration file.
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        # Load About and Module info from settings.py in the config folder
        self.about_info = app_settings.about_info
        self.modules = app_settings.modules

        # Ensure the config directory exists
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            logging.info(f"Created config directory: {config_dir}")

        # Load the config.ini file for APP settings (start_maximized, screen_width, screen_height, etc.)
        if not os.path.exists(self.config_file):
            self.create_default_config()

        self.load_config()

        # Setup logging after loading config
        if self.is_module_enabled('logging'):
            log_file = self.get_logging_setting('log_file', app_settings.logging_defaults['log_file'])
            max_bytes = int(self.get_logging_setting('max_bytes', app_settings.logging_defaults['max_bytes']))  # Default 5MB
            backup_count = int(self.get_logging_setting('backup_count', app_settings.logging_defaults['backup_count']))
            logging_level = self.get_logging_setting('level', app_settings.logging_defaults['level']).upper()

            # Setup logging with the loaded configuration
            setup_logging(log_file=log_file, max_bytes=max_bytes, backup_count=backup_count)

    def load_config(self):
        """
        Loads the application configuration from the config/config.ini file.
        """
        try:
            self.config.read(self.config_file)
            logging.info(f"Configuration loaded from {os.path.normpath(self.config_file)}")
        except Exception as e:
            logging.error(f"Failed to read config file: {e}")

    def create_default_config(self):
        """
        Create a default configuration file for APP settings if it does not exist or is invalid.
        """
        try:
            self.config['APP'] = app_settings.app_defaults
            self.config['LOGGING'] = app_settings.logging_defaults
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
            logging.info(f"Default config created at: {self.config_file}")
        except Exception as e:
            logging.error(f"Failed to create default config: {e}")

    def get_about_info(self, key):
        """
        Get the about information stored in self.about_info.
        
        :param key: The key (name, version, author, etc.) to retrieve.
        :return: The corresponding value from the about_info dictionary.
        """
        return self.about_info.get(key, "Unknown")

    def get_app_setting(self, option, fallback=None):
        """
        Get a setting from the APP section in config.ini for window settings.
        
        :param option: The option (e.g., start_maximized, screen_width, screen_height).
        :param fallback: Fallback value if the option is not found.
        :return: The value of the configuration option or fallback.
        """
        return self.get('APP', option, fallback=fallback)

    def get_logging_setting(self, option, fallback=None):
        """
        Get a logging setting from the LOGGING section in config.ini.
        
        :param option: The logging option (e.g., log_file, max_bytes, level).
        :param fallback: Fallback value if the option is not found.
        :return: The value of the logging configuration option or fallback.
        """
        return self.get('LOGGING', option, fallback=fallback)

    def is_module_enabled(self, module):
        """
        Check if a module is enabled based on settings.
        
        :param module: The module to check (e.g., logging, database).
        :return: True if the module is enabled, False otherwise.
        """
        return self.modules.get(module, False)

    def get(self, section, option, fallback=None):
        """
        Get a configuration value with a fallback if not found.
        
        :param section: The section of the configuration.
        :param option: The option within the section.
        :param fallback: The fallback value if the option is not found.
        :return: The value of the configuration option or fallback.
        """
        try:
            return self.config.get(section, option, fallback=fallback)
        except configparser.NoSectionError:
            logging.error(f"Section '{section}' not found in config file.")
        except configparser.NoOptionError:
            logging.error(f"Option '{option}' not found in section '{section}' of config file.")
        return fallback
