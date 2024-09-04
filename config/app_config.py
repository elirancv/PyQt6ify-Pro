import configparser
import os
import logging

class Config:
    def __init__(self, config_file='config/config.ini'):
        """
        Initialize the Config class.
        
        :param config_file: Path to the configuration file.
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        # About details and module settings are controlled from app_config.py (not written to ini)
        self.about_info = {
            'name': 'PyQt6ify Pro',
            'version': '1.0',
            'author': 'Your Name',
            'website': 'https://www.yourwebsite.com',
            'icon': 'resources/icons/app_icon.png'
        }

        # Default module settings controlled directly in app_config.py
        self.modules = {
            'logging': True,
            'database': True,
            'menu': True,
            'toolbar': True,
            'status_bar': True
        }

        # Ensure the config directory exists
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            logging.info(f"Created config directory: {config_dir}")

        # Load the config.ini file for APP settings (start_maximized, screen_width, screen_height)
        if not os.path.exists(self.config_file):
            self.create_default_config()

        self.load_config()

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
            self.config['APP'] = {
                'start_maximized': 'True',
                'screen_width': '800',
                'screen_height': '600'
            }
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

    def is_module_enabled(self, module):
        """
        Check if a module is enabled based on app_config.py settings.
        
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
