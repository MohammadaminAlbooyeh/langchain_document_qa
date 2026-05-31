from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import secrets
import hashlib

auth_router = APIRouter()

API_KEYS: dict[str, str] = {}
API_KEY_ENABLED = False


def generate_api_key() -> str:
    return f"lq-{secrets.token_hex(24)}"


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user_id: str


class APIKeyResponse(BaseModel):
    api_key: str
    message: str


@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    if not request.email or not request.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    user_id = hashlib.sha256(request.email.encode()).hexdigest()[:16]
    api_key = generate_api_key()
    API_KEYS[api_key] = user_id
    return LoginResponse(token=api_key, user_id=user_id)


@auth_router.post("/verify")
async def verify_key(x_api_key: str = Header(...)):
    if x_api_key in API_KEYS:
        return {"valid": True, "user_id": API_KEYS[x_api_key]}
    raise HTTPException(status_code=401, detail="Invalid API key")


@auth_router.get("/keys")
async def list_keys():
    return {"keys": list(API_KEYS.keys())}
