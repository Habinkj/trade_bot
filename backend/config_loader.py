import json
import os

def load_watchlist():
    """
    Resilient Watchlist Loader for multi-day stability.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "config", "watchlist.json")

    if not os.path.exists(file_path):
        print(f"⚠️ Watchlist not found at {file_path}")
        return []

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"❌ Error loading watchlist: {e}")
        return []