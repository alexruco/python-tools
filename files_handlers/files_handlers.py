import os
import json

def get_project_root(marker='main.py'):
    """Get the root directory of the project by looking for a specific marker file."""
    current_path = os.path.abspath(__file__)
    while True:
        parent_path = os.path.dirname(current_path)
        if os.path.isfile(os.path.join(parent_path, marker)) or current_path == parent_path:
            return parent_path
        current_path = parent_path

def ensure_file_exists(filepath):
    """Ensure the file exists, creating it if necessary."""
    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            json.dump({}, file)