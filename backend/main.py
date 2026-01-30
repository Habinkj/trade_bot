import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from kiteconnect import KiteConnect

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

app = FastAPI()