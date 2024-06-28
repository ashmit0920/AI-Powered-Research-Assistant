import json
import bcrypt

def load_credentials(filename):
    with open(filename, 'r') as f:
        credentials = json.load(f)
    return credentials

def save_credentials(credentials, filename):
    with open(filename, 'w') as f:
        json.dump(credentials, f, indent=4)

def register_user(username, password, filename):
    credentials = load_credentials(filename)

    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    credentials['users'].append({
        'username': username,
        'password': hash.decode('utf-8')
    })
    save_credentials(credentials, filename)

def login_user(username, password, filename):
    credentials = load_credentials(filename)

    bytes = password.encode('utf-8')

    for user in credentials['users']:
        if user['username'] == username and bcrypt.checkpw(bytes, user['password'].encode('utf-8')):
            return True
    return False

def store_api(username, api_key, filename):
    credentials = load_credentials(filename)
    for user in credentials['users']:
        if user['username'] == username:
            user['api'] == api_key

    save_credentials(credentials, filename)