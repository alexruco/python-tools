import re

def extract_urls(text):
    """Extract all URLs from the given text."""
    return re.findall(r'https?://\S+', text)

def log_error(message, log_file='error.log'):
    """Log an error message to a file."""
    with open(log_file, 'a') as file:
        file.write(f"{message}\n")
