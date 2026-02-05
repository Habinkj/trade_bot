import os

TOKEN_FILE = "access_token.txt"

def save_access_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def get_access_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        return f.read().strip()