from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel

router = APIRouter()

# ---------------- AUTH ----------------
FAKE_USER_DB = {
    "admin": "1234"
}

ACTIVE_TOKENS = set()


class LoginRequest(BaseModel):
    username: str
    password: str


def verify_token(authorization: str = Header(None)):
    if authorization not in ACTIVE_TOKENS:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/login")
def login(data: LoginRequest):
    if FAKE_USER_DB.get(data.username) == data.password:
        token = f"token-{data.username}"
        ACTIVE_TOKENS.add(token)
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# ---------------- BOT ENDPOINTS ----------------

@router.get("/scan")
def scan_market(user=Depends(verify_token)):
    return {"signals": ["INFY BUY", "TCS SELL", "HDFCBANK BUY"]}


@router.post("/order")
def place_order(order: dict, user=Depends(verify_token)):
    return {"status": "Order received", "order": order}


@router.get("/status")
def status():
    return {"bot": "running", "market": "open"}