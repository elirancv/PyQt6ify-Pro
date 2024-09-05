import os
from PyQt6.QtWidgets import QMenuBar, QMainWindow
from PyQt6.QtGui import QIcon, QAction, QActionGroup
import logging
from modules import status_bar, about, themes


def update_status_bar(status_bar, message):
    """
    Update the status bar with the provided message.

    :param status_bar: The status bar of the window.
    :param message: The message to display on the status bar.
    """
    if status_bar:
        status_bar.showMessage(message, 5000)  # Show message for 5 seconds
        logging.info(f"Status bar updated: {message}")
    else:
        logging.warning("Failed to update status bar: Status bar not initialized.")


def create_menu(window, config):
    """
    Create a default menu for the application window with icons for each option, 
    including the dynamic listing of available themes and the ability to 
    indicate the currently selected theme with a checkmark.

    :param window: The main application window (must be QMainWindow).
    :param config: The configuration object for the application.
    """
    try:
        # Define paths for icons and styles to avoid repetition
        icons_path = 'resources/icons'
        styles_path = 'resources/styles'

        menubar = QMenuBar(window)
        
        # File menu setup
        file_menu = menubar.addMenu('File')
        new_action = QAction(QIcon(f'{icons_path}/new.png'), 'New', window)
        open_action = QAction(QIcon(f'{icons_path}/open.png'), 'Open', window)
        save_action = QAction(QIcon(f'{icons_path}/save.png'), 'Save', window)
        exit_action = QAction(QIcon(f'{icons_path}/exit.png'), 'Exit', window)
        exit_action.triggered.connect(window.close)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Edit menu setup
        edit_menu = menubar.addMenu('Edit')
        undo_action = QAction(QIcon(f'{icons_path}/undo.png'), 'Undo', window)
        redo_action = QAction(QIcon(f'{icons_path}/redo.png'), 'Redo', window)
        cut_action = QAction(QIcon(f'{icons_path}/cut.png'), 'Cut', window)
        copy_action = QAction(QIcon(f'{icons_path}/copy.png'), 'Copy', window)
        paste_action = QAction(QIcon(f'{icons_path}/paste.png'), 'Paste', window)
        
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        
        # Settings menu setup (with Dynamic Themes)
        settings_menu = menubar.addMenu(QIcon(f'{icons_path}/settings.png'), 'Settings')
        
        # Create a sub-menu for Themes with an icon
        theme_menu = settings_menu.addMenu(QIcon(f'{icons_path}/themes.png'), 'Themes')

        # Create a QActionGroup for exclusive selection of themes
        theme_group = QActionGroup(window)
        theme_group.setExclusive(True)
        
        # Ensure the styles directory exists
        if not os.path.exists(styles_path):
            os.makedirs(styles_path)

        # List all .json theme files in the styles folder
        theme_files = [f for f in os.listdir(styles_path) if f.endswith('.json')]

        # Track the currently selected theme (optional: load it from config or default)
        selected_theme = None
        
        # Add each theme to the theme_menu with an icon
        for theme_file in theme_files:
            theme_name = os.path.splitext(theme_file)[0]  # Get theme name without extension
            theme_action = QAction(QIcon(f'{icons_path}/{theme_name}.png'), theme_name, window)  # Add theme icon
            theme_action.setCheckable(True)  # Make the action checkable
            
            # Add the theme_action to the theme_group
            theme_group.addAction(theme_action)
            
            # Connect each theme action to apply the selected theme, fixing lambda scope issue
            theme_action.triggered.connect(lambda checked, t=os.path.join(styles_path, theme_file), name=theme_name, action=theme_action: apply_selected_theme(window, t, action, name))
            
            # Add the action to the menu
            theme_menu.addAction(theme_action)

            # Mark the theme as selected if it matches the current theme
            if theme_name == selected_theme:
                theme_action.setChecked(True)
        
        # Help menu setup
        help_menu = menubar.addMenu('Help')
        about_action = QAction(QIcon(f'{icons_path}/about.png'), 'About', window)
        about_action.triggered.connect(lambda: about.show_about_dialog(window, config))
        help_menu.addAction(about_action)
        
        # Set the menubar in the window
        window.setMenuBar(menubar)
        logging.info("Menu created successfully.")
        
        # Connect actions to update the status bar
        connect_menu_actions(new_action, "New file created", window)
        connect_menu_actions(open_action, "File opened", window)
        connect_menu_actions(save_action, "File saved", window)
        connect_menu_actions(undo_action, "Undo action", window)
        connect_menu_actions(redo_action, "Redo action", window)
        connect_menu_actions(cut_action, "Cut action", window)
        connect_menu_actions(copy_action, "Copy action", window)
        connect_menu_actions(paste_action, "Paste action", window)
        connect_menu_actions(about_action, "Opened About dialog", window)

    except Exception as e:
        logging.error(f"Failed to create menu: {e}", exc_info=True)


def apply_selected_theme(window, theme_file, theme_action, theme_name):
    """
    Applies the selected theme and updates the checkmark in the menu.

    :param window: The main application window.
    :param theme_file: Path to the selected theme JSON file.
    :param theme_action: The QAction representing the selected theme.
    :param theme_name: The name of the selected theme.
    """
    try:
        # Apply the selected theme
        themes.apply_theme(window.app, theme_file)
        
        # Mark this action as selected (the QActionGroup ensures only one is selected)
        theme_action.setChecked(True)
        
        # Update status bar to indicate the theme has been applied
        update_status_bar(window.statusBar(), f"Theme applied: {theme_name}")
        logging.info(f"Theme applied: {theme_name}")

    except Exception as e:
        logging.error(f"Failed to apply theme: {e}", exc_info=True)


def connect_menu_actions(action, message, window):
    """
    Connects a menu action to update the status bar with a specific message.

    :param action: The QAction to connect.
    :param message: The message to display when the action is triggered.
    :param window: The main application window (must have a status bar).
    """
    try:
        action.triggered.connect(lambda: update_status_bar(window.statusBar(), message))
    except Exception as e:
        logging.error(f"Failed to connect action '{action.text()}': {e}", exc_info=True)
