from fastapi import Request, HTTPException
from services.auth import get_user_id_from_token


async def get_user_id(request: Request) -> int | None:
    """Extract user_id from Bearer token. Returns None if no token provided."""
    auth = request.headers.get("authorization", "")
    if auth.startswith("Bearer "):
        return await get_user_id_from_token(auth[7:])
    return None


async def require_user_id(request: Request) -> int:
    """Extract user_id from Bearer token. Raises 401 if missing/invalid."""
    user_id = await get_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id
