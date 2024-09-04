"""
## PyQt6ify Pro

**PyQt6ify Pro** is a template designed to streamline the creation of new applications using **PyQt6**. It provides a ready-to-use framework that includes a modular design for menus, toolbars, status bars, logging, and database integration. The project combines ease of setup with flexibility, making it a perfect starting point for developing PyQt6 applications.

## Features

- **App Information**:
  - Application name, version, author, and website are hardcoded in `app_config.py`.
  - Easily update these settings within the Python file for consistent use across the application.

- **Window Settings**:
  - Configurable window settings via `config.ini`, including:
    - `start_maximized`: Whether the app starts maximized.
    - `screen_width` & `screen_height`: Default dimensions of the application window.

- **Modular Components**:
  - **Menu**:
    - Pre-configured File, Edit, and Help menus with core actions like New, Open, Save, and About.
  - **Toolbar**:
    - Icons for File operations (New, Open, Save) and Edit actions (Undo, Redo, Cut, Copy, Paste).
  - **Status Bar**:
    - Provides temporary and permanent messages for user feedback, including real-time status updates for actions.
  - **Database**:
    - Integrated SQLite database setup for persistent storage and application data management.
  - **Logging**:
    - Logs both to a file (`logs/app.log`) and the console. Logs key application actions and errors for easier debugging and maintenance.

## Getting Started

1. **Clone the repository**:
   git clone https://github.com/elirancv/PyQt6ify-Pro
   cd PyQt6ify-Pro

2.	Install the requirements: Install the dependencies specified in requirements.txt:
pip install -r requirements.txt

3.	Run the application: Launch the PyQt6 application by executing main.py:
python main.py
Configuration
•	Application Settings:
o	App Information is hardcoded in app_config.py and includes:
	name: Application name (default: "MyApp").
	version: Application version (default: "1.0").
	author: The author of the application.
	website: The official website link for the application.
•	Window Settings:
o	Controlled through config.ini:
	start_maximized: Start the application maximized (True or False).
	screen_width: Default window width.
	screen_height: Default window height.
•	Modules:
o	Enable or disable modules such as logging, database, menu, toolbar, and status_bar in app_config.py.

## How to Contribute
Contributions are welcome! If you have ideas or improvements, feel free to:

1.	Fork the repository.
2.	Create a new branch (git checkout -b feature-branch).
3.	Commit your changes (git commit -m 'Add a new feature').
4.	Push to your branch (git push origin feature-branch).
5.	Create a pull request.

## License
This project is licensed under the MIT License. Feel free to use it as a starting point for your own PyQt6 projects.
Version
v1.0.0 b001 (2024-09-04) """
