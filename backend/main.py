from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os
from kiteconnect import KiteConnect

app = FastAPI()


# CORS (allows frontend or external apps to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend domain later for security

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root route (REQUIRED for Render to know app is alive)
@app.get("/")
def root():
    return {"status": "Trade bot API running"}

# Trading signal route
@app.get("/signal/{symbol}")
def get_signal(symbol: str):
    return generate_signal(symbol)

API_KEY = os.getenv("ap8yn60ef82vf3hh")
API_SECRET = os.getenv("from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os
from kiteconnect import KiteConnect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key=API_KEY)


@app.get("/")
def home():
    return {"message": "Trade bot API is running"}


# 🔐 Step 1: Redirect user to Zerodha login
@app.get("/login")
def login():
    login_url = kite.login_url()
    return RedirectResponse(login_url)


# 🔁 Step 2: Zerodha redirects back here after login
@app.get("/callback")
def callback(request: Request):
    request_token = request.query_params.get("request_token")

    data = kite.generate_session(request_token, api_secret=API_SECRET)
    kite.set_access_token(data["access_token"])

    return {
        "status": "Login successful",
        "access_token": data["access_token"]
    }
")

kite = KiteConnect(api_key=API_KEY)


@app.get("/")
def home():
    return {"message": "Trade bot API is running"}


# 🔐 Step 1: Redirect user to Zerodha login
@app.get("/login")
def login():
    login_url = kite.login_url()
    return RedirectResponse(login_url)


# 🔁 Step 2: Zerodha redirects back here after login
@app.get("/callback")
def callback(request: Request):
    request_token = request.query_params.get("request_token")

    data = kite.generate_session(request_token, api_secret=API_SECRET)
    kite.set_access_token(data["access_token"])

    return {
        "status": "Login successful",
        "access_token": data["access_token"]
    }

