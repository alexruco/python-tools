# model_interaction.py

import requests
import json


def generate_response(prompt, model_url="http://localhost:11434/api/generate", model_name="llama3"):
    """Generate a response from the specified model given a prompt."""
    payload = {"model": model_name, "prompt": prompt}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(model_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return parse_response(response.text)
    except requests.RequestException as e:
        print(f"Failed to generate response: {e}")
        return ""



def check_model_status(model_url="http://localhost:11434/api/generate", model_name="llama3"):
    """Check if the model is running by sending a request to the API."""
    payload = {"model": model_name, "prompt": "Test prompt to check status."}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(model_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Failed to connect to model API: {e}")
        return False

def parse_response(response_text):
    """Parse the JSON lines response from the API."""
    response_lines = response_text.strip().split('\n')
    full_response = ""

    for line in response_lines:
        try:
            response_json = json.loads(line)
            full_response += response_json.get('response', '')
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON line: {e.msg}")
            print(f"Line content: {line}")

    return full_response
