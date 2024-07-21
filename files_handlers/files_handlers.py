import os
import json

def ensure_file_exists(filepath):
    """Ensure the file exists, creating it if necessary."""
    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            json.dump({}, file)