import logging
from PyQt6.QtWidgets import QToolBar, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from modules.status_bar import update_status_bar

def create_toolbar(window):
    """
    Create a default toolbar for the application window with icons for each option and right-click options to toggle the visibility of groups.

    :param window: The main application window.
    """
    try:
        toolbar = QToolBar("Main Toolbar")
        window.addToolBar(toolbar)

        # File actions
        new_action = QAction(QIcon('resources/icons/new.png'), 'New', window)
        open_action = QAction(QIcon('resources/icons/open.png'), 'Open', window)
        save_action = QAction(QIcon('resources/icons/save.png'), 'Save', window)
        
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        
        # Edit actions
        undo_action = QAction(QIcon('resources/icons/undo.png'), 'Undo', window)
        redo_action = QAction(QIcon('resources/icons/redo.png'), 'Redo', window)
        cut_action = QAction(QIcon('resources/icons/cut.png'), 'Cut', window)
        copy_action = QAction(QIcon('resources/icons/copy.png'), 'Copy', window)
        paste_action = QAction(QIcon('resources/icons/paste.png'), 'Paste', window)
        
        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)
        toolbar.addSeparator()
        toolbar.addAction(cut_action)
        toolbar.addAction(copy_action)
        toolbar.addAction(paste_action)
        toolbar.addSeparator()
        
        # Exit action
        exit_action = QAction(QIcon('resources/icons/exit.png'), 'Exit', window)
        exit_action.triggered.connect(window.close)
        toolbar.addAction(exit_action)
        
        logging.info("Toolbar created successfully")

        # Group actions for visibility toggling
        file_actions = [new_action, open_action, save_action]
        edit_actions = [undo_action, redo_action, cut_action, copy_action, paste_action]

        # Add right-click context menu to toggle File/Edit actions visibility
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        toolbar.customContextMenuRequested.connect(lambda pos: show_toolbar_context_menu(toolbar, pos, file_actions, edit_actions))

        # Connect actions to status bar updates
        new_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "New file created"))
        open_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "File opened"))
        save_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "File saved"))
        undo_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Undo action"))
        redo_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Redo action"))
        cut_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Cut action"))
        copy_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Copy action"))
        paste_action.triggered.connect(lambda: update_status_bar(window.statusBar(), "Paste action"))
        
    except Exception as e:
        logging.error(f"Failed to create toolbar: {e}")

def show_toolbar_context_menu(toolbar, pos, file_actions, edit_actions):
    """
    Display a context menu for toggling the visibility of File and Edit actions on the toolbar, and an option to reset the toolbar to its default state.

    :param toolbar: The toolbar widget.
    :param pos: The position where the right-click occurred.
    :param file_actions: The list of file-related actions.
    :param edit_actions: The list of edit-related actions.
    """
    menu = QMenu(toolbar)

    # Toggle File actions visibility
    file_action_toggle = menu.addAction("Show File Actions")
    file_action_toggle.setCheckable(True)
    file_action_toggle.setChecked(all(action.isVisible() for action in file_actions))
    file_action_toggle.triggered.connect(lambda: toggle_action_visibility(file_actions))

    # Toggle Edit actions visibility
    edit_action_toggle = menu.addAction("Show Edit Actions")
    edit_action_toggle.setCheckable(True)
    edit_action_toggle.setChecked(all(action.isVisible() for action in edit_actions))
    edit_action_toggle.triggered.connect(lambda: toggle_action_visibility(edit_actions))

    # Reset toolbar action
    reset_action = menu.addAction("Reset Toolbar")
    reset_action.triggered.connect(lambda: reset_toolbar(file_actions, edit_actions))

    # Show the context menu at the clicked position
    menu.exec(toolbar.mapToGlobal(pos))

def toggle_action_visibility(actions):
    """
    Toggle the visibility of a list of actions.

    :param actions: A list of QAction objects to toggle visibility.
    """
    if all(action.isVisible() for action in actions):
        for action in actions:
            action.setVisible(False)
    else:
        for action in actions:
            action.setVisible(True)

def reset_toolbar(file_actions, edit_actions):
    """
    Reset the toolbar by making all actions visible.

    :param file_actions: The list of file-related actions.
    :param edit_actions: The list of edit-related actions.
    """
    for action in file_actions + edit_actions:
        action.setVisible(True)
    logging.info("Toolbar has been reset to default.")
