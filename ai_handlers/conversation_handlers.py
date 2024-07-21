import json
import os
import re
from files_handlers import ensure_file_exists
from files_handlers import get_project_root
from misc_handlers import log_error
from web_handlers import encode_urls


def store_conversation(conversation, hashtags, filename='conversations.json'):
    """Store conversation into a JSON file organized by hashtags."""
    if not hashtags or not conversation:
        return

    # Encode URLs in the conversation before storing
    conversation['prompt'] = encode_urls(conversation['prompt'])
    conversation['response'] = encode_urls(conversation['response'])

    project_root = get_project_root()
    filepath = os.path.join(project_root, filename)

    ensure_file_exists(filepath)

    data = {}
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                data = json.load(file)
    except json.JSONDecodeError:
        data = {}
        log_error(f"File {filepath} is empty or contains invalid JSON. Initializing with empty dictionary.")

    if not isinstance(data, dict):
        data = {}

    for hashtag in hashtags:
        data.setdefault(hashtag, []).append(conversation)

    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def fetch_conversations(hashtags, filename='conversations.json'):
    """Fetch conversations for given hashtags from a JSON file."""
    project_root = get_project_root()
    filepath = os.path.join(project_root, filename)

    ensure_file_exists(filepath)

    data = {}
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        log_error(f"File {filepath} is empty or contains invalid JSON. Returning empty conversations list.")

    conversations = []
    for hashtag in hashtags:
        conversations.extend(data.get(hashtag, []))
    
    return conversations

def remove_hashtags(text):
    """Remove hashtags from the text."""
    return re.sub(r'#\w+', '', text).strip()