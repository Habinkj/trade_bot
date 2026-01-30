from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from kiteconnect import KiteConnect
import os

app = FastAPI()

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=API_KEY)


@app.get("/")
def home():
    return {"message": "Trade bot API is running 🚀"}


@app.get("/login")
def login():
    login_url = kite.login_url()
    return RedirectResponse(login_url)


@app.get("/callback")
def callback(request: Request):
    request_token = request.query_params.get("request_token")

    data = kite.generate_session(request_token, api_secret=API_SECRET)
    kite.set_access_token(data["access_token"])

    return {
        "status": "Login successful",
        "access_token": data["access_token"]
    }