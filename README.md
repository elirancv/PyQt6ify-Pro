## PyQt6ify Pro

**PyQt6ify Pro** is a comprehensive starter kit for building desktop applications with **PyQt6**. It features a modular design with customizable menus, toolbars, status bars, integrated logging, and database support. Whether you're starting a new project or need a structured template, PyQt6ify Pro provides the flexibility and organization needed for efficient development.

<div align="left">
  <img src="./resources/images/screenshot_main.png" alt="Main Screenshot" width="600" />
</div>

<br/>

<div align="left">
  <img src="./resources/images/screenshot_about.png" alt="About Screenshot" width="320" />
</div>

## Key Features

- **App Information**:
  - Manage app name, version, author, and website centrally in `app_config.py` for consistent use across the app.
  - Easily update settings via the built-in **Config Defaults** screen.

- **Window Settings**:
  - Configurable via `config.ini` for app dimensions and startup behavior (e.g., start maximized).

- **Modular Components**:
  - **Menu**: Pre-configured with common actions like New, Open, Save, and About.
  - **Toolbar**: Provides icons for file operations and editing actions.
  - **Status Bar**: Displays real-time messages and updates during user interactions.
  - **Themes**: Choose from a variety of pre-built themes like `Autumn Ember`, `Cyber Steel`, `Dark Theme`, and more, customizable through the settings menu.

- **Database Integration**:
  - Includes built-in SQLite database support for persistent data storage and easy management.

- **Logging**:
  - Dynamic logging configuration through `config.ini`:
    - Supports log rotation, file size limits, backup counts, and multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    - Output to both a log file (`logs/app.log`) and console.



## Getting Started

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/elirancv/PyQt6ify-Pro
    cd PyQt6ify-Pro
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    ```bash
    python main.py
    ```

## Configuration

- **App Settings** (`app_config.py`):
  - `name`: App name (default: **MyApp**).
  - `version`: Version (default: **1.0**).
  - `author`: Author name (default: **Your Name**).
  - `website`: Website URL.

- **Window Settings** (`config.ini`):
  - `start_maximized`: Start app maximized (`True/False`).
  - `screen_width` & `screen_height`: Window dimensions.

- **Module Control** (`app_config.py`):
  - Enable or disable specific features like logging, database, menu, toolbar, and status bar.

## Logging Configuration

- **Logging Settings** (`config.ini`):
  - `log_file`: Log file path (default: `logs/app.log`).
  - `max_bytes`: Max log file size (default: `5MB`).
  - `backup_count`: Number of backup log files (default: `3`).
  - `level`: Logging level (default: `INFO`).

## Contributing

We welcome contributions! To contribute:
1. **Fork the repository** and create a new branch:  
   `git checkout -b feature-branch`
2. **Commit your changes**:  
   `git commit -m "Add new feature"`
3. **Push your branch**:  
   `git push origin feature-branch`
4. **Submit a pull request** for review.

We’ll review and merge it once ready.

## License

This project is licensed under the MIT License. You are free to use **PyQt6ify Pro** for your own projects.

## Version

`v1.0.0 b002 (2024-09-05)`
