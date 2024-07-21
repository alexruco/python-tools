import json
import os
from files_handlers import get_project_root


def store_role_data(role, data, filename='roles.json'):
    """Store role data into a JSON file."""
    if not role or not data:
        return

    project_root = get_project_root()
    filepath = os.path.join(project_root, filename)

    roles = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            roles = json.load(file)
    
    roles.setdefault(role, []).append(data)

    with open(filepath, 'w') as file:
        json.dump(roles, file, indent=4)

def fetch_role_data(role, filename='roles.json'):
    """Fetch data for a given role from a JSON file."""
    project_root = get_project_root()
    filepath = os.path.join(project_root, filename)

    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r') as file:
        roles = json.load(file)
        return roles.get(role, [])

def set_standard_role(standard_role, filename='roles.json'):
    """Set the standard role and remove it from any other roles."""
    if not standard_role:
        return

    project_root = get_project_root()
    filepath = os.path.join(project_root, filename)

    roles = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            roles = json.load(file)

    for role in roles:
        if 'standard_role' in roles[role]:
            roles[role].remove('standard_role')

    roles.setdefault(standard_role, []).append('standard_role')

    with open(filepath, 'w') as file:
        json.dump(roles, file, indent=4)

def handle_standard_role(prompt):

    standard_role_pattern = re.compile(r'\[standard_role:@(\w+)\]')
    standard_role_match = standard_role_pattern.search(prompt)

    if standard_role_match:
        standard_role = standard_role_match.group(1)
        set_standard_role(standard_role)
        prompt = standard_role_pattern.sub('', prompt)
    
    return prompt

def handle_roles(prompt):
    role_pattern = re.compile(r'\[@(\w+):([^\]]*)\]')
    roles = role_pattern.findall(prompt)
    role_data = ""

    for role, data in roles:
        if data:
            store_role_data(role, data)
        fetched_role_data = fetch_role_data(role)
        if not fetched_role_data:
            store_role_data(role, "No specific data provided")  # Storing a placeholder if no data is provided
            fetched_role_data = fetch_role_data(role)
        role_data += "\n".join(fetched_role_data) + "\n"

    simple_role_pattern = re.compile(r'\[@(\w+)\]')
    simple_roles = simple_role_pattern.findall(prompt)

    for role in simple_roles:
        fetched_role_data = fetch_role_data(role)
        if not fetched_role_data:
            store_role_data(role, "No specific data provided")  # Storing a placeholder if no data is provided
            fetched_role_data = fetch_role_data(role)
        role_data += "\n".join(fetched_role_data) + "\n"
    
    return role_data
