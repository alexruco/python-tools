import os
import json

def get_project_root():
    """Get the root directory of the project."""
    return os.path.dirname(os.path.abspath(__file__))

def ensure_file_exists(filepath):
    """Ensure the file exists, creating it if necessary."""
    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            json.dump({}, file)