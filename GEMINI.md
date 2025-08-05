# Gemini Agent Instructions for quickcmd

This document provides instructions for the Gemini agent on how to interact with, develop, and manage the `quickcmd` project.

## Project Overview

`quickcmd` is a command-line utility designed to simplify the management and execution of custom commands. It uses `fzf` for fuzzy-finding through commands defined in `.ini` files, allowing for quick, interactive execution. The core logic is written in Python, with a `bash` script acting as the main entry point and wrapper.

## Core Technologies

- **Language**: Python 2/3, Bash
- **Key Libraries**: `requests`, `urllib3`
- **Core Tools**: `fzf` (a command-line fuzzy finder)
- **Configuration**: `.ini` files for command definitions.
- **Testing**: Standard Python `unittest` module.

## Project Structure

- `quickcmd.sh`: The main entry point script that the user sources and calls via the `qc` function. It handles locating the python interpreter and executing the main python script.
- `src/`: Contains all Python source code.
  - `quickcmd.py`: The main Python script that parses arguments and orchestrates the application flow.
  - `command_manager.py`: Handles loading, adding, deleting, and modifying commands from `.ini` files.
  - `command.py`: Represents a single command object.
  - `fzf.py`: A wrapper for interacting with the `fzf` command-line tool.
  - `iniparser.py`: Custom parser for the `.ini` configuration files.
- `commands/`: The default directory where user-defined command `.ini` files are stored.
- `test/`: Contains unit tests.
- `install.sh`: Script for installing `quickcmd` and its dependencies (`fzf`, python packages).
- `requirements.txt`: Python dependencies.

## Development Workflow

### 1. Install Dependencies

The project requires Python and the packages listed in `requirements.txt`. `fzf` is also a critical dependency.

To install Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Running the Application

The application is intended to be run via the `qc` function defined in `quickcmd.sh`. For development and testing, you can execute the main Python script directly:

```bash
python src/quickcmd.py
```

To list all commands without using `fzf`:
```bash
python src/quickcmd.py --list
```

### 3. Running Tests

Tests are located in the `test/` directory and can be run using Python's `unittest` module.

```bash
python -m unittest discover test
```

### 4. Managing Commands

- **Location**: Commands are stored in `.ini` files within the `commands/` directory.
- **Adding a Command**: New commands can be added by creating a new `.ini` file or adding a new section to an existing one in the `commands/` directory. The interactive way is to run `python src/quickcmd.py --addcmd`.
- **Structure of a command in `.ini`**:
  ```ini
  [command_name]
  command = echo "Hello, World!"
  workdir = /tmp
  tip = A simple example command.
  ```

## Goals for Gemini

Your primary tasks for this project will be:

1.  **Bug Fixes**: Identify and fix bugs in the Python source code (`src/`) or the `quickcmd.sh` script.
2.  **Feature Development**: Add new features, such as new command types, enhanced configuration options, or improved output formatting.
3.  **Refactoring**: Improve code quality, such as refactoring the `iniparser.py` or improving the command execution logic in `command_manager.py`.
4.  **Writing Tests**: Add new unit tests in the `test/` directory to cover new or existing functionality.
5.  **Managing Commands**: Assist with creating, modifying, or deleting commands in the `commands/` directory as requested.
