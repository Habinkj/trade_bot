import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from kiteconnect import KiteConnect

app = FastAPI()

# Load API credentials from Render environment variables
API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")

if not API_KEY or not API_SECRET:
    raise Exception("API keys not set in environment variables")

kite = KiteConnect(api_key=API_KEY)


@app.get("/")
def home():
    return {"message": "Trade bot API is running 🚀"}


# Step 1 — Redirect user to Zerodha login
@app.get("/login")
def login():
    login_url = kite.login_url()
    return RedirectResponse(login_url)


# Step 2 — Zerodha redirects back here after login
@app.get("/callback")
def callback(request: Request):
    request_token = request.query_params.get("request_token")

    if not request_token:
        raise HTTPException(status_code=400, detail="Request token missing")

    try:
        # Exchange request_token for access_token
        data = kite.generate_session(request_token, api_secret=API_SECRET)
        access_token = data["access_token"]

        kite.set_access_token(access_token)

        return {
            "status": "Login successful ✅",
            "access_token": access_token
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))