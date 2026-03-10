from fastapi import APIRouter
from models.schemas import AuthRequest, AuthResponse
from services.auth import get_or_create_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(req: AuthRequest):
    result = await get_or_create_user(req.username)
    return AuthResponse(**result)


@router.post("/login", response_model=AuthResponse)
async def login(req: AuthRequest):
    result = await get_or_create_user(req.username)
    return AuthResponse(**result)
