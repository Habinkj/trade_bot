import json

def load_watchlist():
    with open("config/watchlist.json", "r") as f:
        return json.load(f)