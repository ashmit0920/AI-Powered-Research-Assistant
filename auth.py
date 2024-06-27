import json

def load_credentials(filename):
    with open(filename, 'r') as f:
        credentials = json.load(f)
    return credentials

def save_credentials(credentials, filename):
    with open(filename, 'w') as f:
        json.dump(credentials, f, indent=4)

def register_user(username, password, filename):
    credentials = load_credentials(filename)
    credentials['users'].append({
        'username': username,
        'password': password
    })
    save_credentials(credentials, filename)

def login_user(username, password, filename):
    credentials = load_credentials(filename)
    for user in credentials['users']:
        if user['username'] == username and user['password'] == password:
            return True
    return False
