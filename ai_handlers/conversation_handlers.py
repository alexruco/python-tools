#conversation_handlers

import json
import os
import re
from files_handlers import ensure_file_exists
from misc_handlers import log_error
from web_handlers import encode_urls

def store_conversation(conversation, hashtags, project_root, filename):
    """Store conversation into a JSON file organized by hashtags."""
    if not hashtags or not conversation:
        return

    # Encode URLs in the conversation before storing
    conversation['prompt'] = encode_urls(conversation['prompt'])
    conversation['response'] = encode_urls(conversation['response'])

    #project_root = get_project_root()
    print(f"Project root: {project_root}")  # Debugging: Print the project root

    filepath = os.path.join(project_root, filename)
    print(f"File path: {filepath}")  # Debugging: Print the full file path

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
        
def fetch_conversations(hashtags, project_root, filename='conversations.json'):
    """Fetch conversations for given hashtags from a JSON file."""
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

def handle_hashtags(prompt, project_root):
    hashtag_pattern = re.compile(r'#(\w+)')
    hashtags = hashtag_pattern.findall(prompt)
    conversations = fetch_conversations(hashtags, project_root)
    
    # Convert each conversation to a string format
    formatted_conversations = []
    for convo in conversations:
        formatted_conversations.append(f"Past question: {convo['prompt']}\nPast response: {convo['response']}")
    
    return hashtags, "\n".join(formatted_conversations)


def remove_hashtags(text):
    """Remove hashtags from the text."""
    return re.sub(r'#\w+', '', text).strip()