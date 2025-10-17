from enum import Enum
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Optional

# Define the scopes from the original implementation
class Scopes(str, Enum):
    GymSuperAdmin = "gym:superadmin"
    GymAdmin = "gym:admin"
    GymWorker = "gym:worker"

# Mock database for development
class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = False
    scopes: List[str] = []
    id_gym: Optional[str] = None  # Added to match the original implementation
    id: str = ""  # Added to match the original implementation

# Mock user database with scopes matching the original implementation
MOCK_USERS = {
    "superadmin": {
        "username": "superadmin",
        "email": "superadmin@example.com",
        "full_name": "Super Admin User",
        "disabled": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "scopes": [Scopes.GymSuperAdmin],
        "id_gym": "00000000-0000-0000-0000-000000000000",
        "id": "11111111-1111-1111-1111-111111111111"
    },
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "disabled": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "scopes": [Scopes.GymAdmin],
        "id_gym": "00000000-0000-0000-0000-000000000000",
        "id": "22222222-2222-2222-2222-222222222222"
    },
    "worker": {
        "username": "worker",
        "email": "worker@example.com",
        "full_name": "Gym Worker",
        "disabled": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "scopes": [Scopes.GymWorker],
        "id_gym": "00000000-0000-0000-0000-000000000000",
        "id": "33333333-3333-3333-3333-333333333333"
    }
}

bearer_schema = HTTPBearer()

def fake_decode_token(token):
    # This doesn't provide any security at all
    print(token, "Hola mundo ")
    user = {
        "username": "worker",
        "email": "worker@example.com",
        "full_name": "Gym Worker",
        "disabled": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "scopes": [Scopes.GymWorker],
        "id_gym": "00000000-0000-0000-0000-000000000000",
        "id": "33333333-3333-3333-3333-333333333333"
    }
    return User(**user)

async def get_current_user(token: str = Depends(bearer_schema)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def has_required_scopes(required_scopes: list, user_scopes: list) -> bool:
    """Check if user has at least one of the required scopes"""
    return any(scope in user_scopes for scope in required_scopes)

def get_user_scopes(username: str) -> list:
    """Get scopes for a specific user"""
    user = MOCK_USERS.get(username)
    if not user:
        return []
    return user.get("scopes", [])
