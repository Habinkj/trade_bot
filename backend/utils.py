from dhanhq import dhanhq
import os
import yaml

def load_config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

def get_dhan_credentials():
    return {
        "client_id": os.getenv("DHAN_CLIENT_ID"),
        "access_token": os.getenv("DHAN_ACCESS_TOKEN")
    }

def get_dhan_client():
    creds = get_dhan_credentials()
    return dhanhq(creds["client_id"], creds["access_token"])
